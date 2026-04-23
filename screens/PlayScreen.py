import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from screens.screen import Screen

class PlayScreen(Screen):
    """
    README - PlayScreen

    Description:
    This class defines the main shared gameplay logic for the SET game play screen.
    It manages the board display, player action timer, whole game timer, pause/resume
    behavior, status messages, background image, and sound effects.
    It is designed as a base play screen that can support both multiplayer and
    singleplayer game modes.

    Parameters:
    game:
        The main Game object.
        It provides shared resources and state such as:
        - fonts
        - current screen
        - table object
        - turn duration
        - score rules
        - screen switching

    Structure:
        - Inherits from Screen
        - Uses Display_board to draw the cards/table
        - Uses pygame.Rect objects for buttons
        - Tracks active answering player
        - Tracks 15-second SET answering timer
        - Tracks full game timer
        - Supports game pause and resume
        - Stores temporary status messages
        - Loads background image and sound effects

    Output:
        The class itself does not directly return a final output value.
        Instead, it updates and manages internal game state, including:
        - timer values
        - current active player
        - winner state
        - pause state
        - displayed messages
        - table selection state

    """
    def __init__(self, game):
        """Initialize the shared play screen state, timers, assets, and controls."""
        super().__init__(game)
        self.board = Display_board(game)
        self.setbutton = pygame.Rect(200, 80, 198, 80)
        self.hint_button = pygame.Rect(0, 0, 100, 40)
        self.restart_button = pygame.Rect(0, 0, 100, 50)
        self.menu_button = pygame.Rect(0, 0, 100, 50)
        self.active_player = None

        # 15-second SET timer
        self.set_time_limit = 15000
        self.set_start_time = 0

        # winner
        self.winner = None

        # Game pause timer
        self.paused = False
        self.pause_start_time = 0

        # Message panel
        self.status_message = "Press set when ready"
        self.message_end_time = 0

        # Whole game timer: 5 mins (Default)
        self.game_duration = self.game.turn_duration_ms + 1000
        self.game_start_time = pygame.time.get_ticks()

        # Background
        img = pygame.image.load("images/table.png").convert()
        img_w, img_h = img.get_size()
        screen_w, screen_h = 1080, 720
        x = (img_w - screen_w) // 2
        y = (img_h - screen_h) // 2
        self.background = img.subsurface((x, y, screen_w, screen_h))

        #Configure sounds
        try:
            self.correct_sound = pygame.mixer.Sound("sounds/correct.wav")
            self.wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")
            self.select_sound = pygame.mixer.Sound("sounds/select.wav")
            self.set_sound = pygame.mixer.Sound("sounds/set.wav")

            # Adjust volume (0.0 to 1.0)
            self.correct_sound.set_volume(0.3)
            self.wrong_sound.set_volume(0.5)
            self.select_sound.set_volume(0.4)
            self.set_sound.set_volume(0.5)

        except Exception as e:
            print(f"Could not load sounds: {e}")
            self.correct_sound = None
            self.wrong_sound = None
            self.set_sound = None
            self.select_sound = None

    def reset_game_screen(self):
        """Reset the play screen state and restart the table and timers."""
        self.winner = None
        self.clear_set_timer()

        self.game_duration = self.game.turn_duration_ms + 1000
        self.game_start_time = pygame.time.get_ticks()

        # very important: clear pause state
        self.paused = False
        self.pause_start_time = 0

        # reset table
        self.game.table.selection_mode = False
        self.game.table.selected = []
        self.game.table.hinted = []
        self.game.table.handle_start_game()


    def start_set_timer(self, player):
        """Start the 15-second answering timer for the given player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()  # it is the time pass when the game start until you click SET button


    def clear_set_timer(self):
        """Stop the answer period."""
        self.active_player = None
        self.set_start_time = 0

    def get_time_left(self):
        """
        Description:
        Calculates and returns the remaining time (in seconds) for the active player's SET attempt.

        Function:
        If no player is currently answering, it returns the default time (15 seconds).
        If the time runs out, it resets the selection, applies a score penalty,
        shows a "Time's up!" message, and clears the timer.
        """

        if self.active_player is None:
            return 15

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.set_start_time
        remaining = self.set_time_limit - elapsed

        if remaining <= 0:
            if self.wrong_sound:
                self.wrong_sound.play()
            # Clear the highlighted cards when time is up!
            self.game.table.selection_mode = False
            self.game.table.selected = []
            self.game.table.hinted = []

            if self.active_player == 1:
                self.p1_score -= self.game.point_loss
            elif self.active_player == 2:
                if self.game.current_screen == self.game.game_screen:
                    self.p2_score -= self.game.point_loss
                else:
                    self.comp_score -= self.game.point_loss

            self.show_message("Time's up!", 1500)
            self.clear_set_timer()
            return 0

        return remaining // 1000 + 1

    # to make sure single player have the same function as multiplayer
    def get_game_time_left(self):
        """Return the remaining overall game time in seconds."""
        if self.paused:
            current_time = self.pause_start_time
        else:
            current_time = pygame.time.get_ticks()

        elapsed = current_time - self.game_start_time
        remaining = self.game_duration - elapsed

        if remaining <= 0:
            return 0

        return remaining // 1000


    def pause_game_timer(self):
        """Pause the overall game timer."""
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()


    def resume_game_timer(self):
        """Resume the overall game timer after a pause."""
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += paused_duration
            self.paused = False


    #show different message based on user action result
    def show_message(self, text, duration=1500):
        """Display a temporary status message for a given duration."""
        self.status_message = text
        self.message_end_time = pygame.time.get_ticks() + duration