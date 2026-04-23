import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
from screens.screen import Screen

class PlayScreen(Screen):
    """
    README - PlayScreen

    Description:
    This class is the base class for playable game screens such as
    singleplayer and multiplayer. It handles shared UI elements,
    timers, sounds, messages, and common game state logic.

    Parameters:
    game:
        The main Game object used to access shared resources,
        table logic, timers, and screen data.

    Structure:
        - Inherits from Screen
        - Creates the game board and shared buttons
        - Manages answer timer and overall game timer
        - Handles pause state and temporary messages
        - Loads background image and sound effects

    Output:
        Provides shared gameplay logic for child classes such as
        SingleplayerScreen and Multiplayer.
    """

    def __init__(self, game):
        """Initialize shared UI elements, timers, background, and sounds."""
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
        """Reset shared timers, pause state, and table state for a new game."""
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
        """Start the 15-second answer timer for the given player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()

    def clear_set_timer(self):
        """Clear the current answer timer and active player."""
        self.active_player = None
        self.set_start_time = 0

    def get_time_left(self):
        """
        Description:
        Calculates the remaining time for the active player's answer turn.

        Function:
        Returns the remaining answer time in seconds. If time runs out,
        it clears selected cards, applies a score penalty, shows a timeout
        message, and resets the active timer.
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

    def get_game_time_left(self):
        """Return the remaining total game time in seconds."""
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

    def show_message(self, text, duration=1500):
        """Store a temporary status message and its display duration."""
        self.status_message = text
        self.message_end_time = pygame.time.get_ticks() + duration