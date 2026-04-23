import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
from screens.screen import Screen

class PlayScreen(Screen):
    '''
    Description:
    Base class for the playable game screens (Singleplayer and Multiplayer). Handles the shared UI components like the board display, buttons (hint, restart, menu), audio playback, and complex timing logic (including the 15-second SET timer, overall game timer, and pause states).
    Parameters:
    game: The central Game object acting as the main controller.
    Limitations:
    Highly coupled to the specific attribute structures of the `Game` and `Table` classes. Audio failure silently disables sound effects instead of throwing a hard error to prevent crashes.
    Structures:
    Inherits from the `Screen` base class. Uses `pygame.Rect` for UI boundaries, `pygame.mixer.Sound` for audio, integers for millisecond timing, and boolean flags for tracking pause and player states.
    Outputs:
    An initialized PlayScreen instance serving as the foundation for specific game modes.
    '''
    def __init__(self, game):
        '''
        Description:
        Initializes the UI rectangles, sets default values for timers, positions the background, and loads the audio assets.
        Parameters:
        game: The main Game object.
        Limitations:
        The background positioning math assumes a base application resolution of 1080x720.
        Structures:
        Calls `super().__init__(game)` to inherit base behaviors. Employs a try-except block to safely load `.wav` files into `pygame.mixer.Sound` objects and set their volumes.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Resets the timing, pause states, and table logic to prepare for a fresh game.
        Parameters:
        None.
        Limitations:
        Does not reset player scores directly within this method (relies on child classes to handle specific scoring logic).
        Structures:
        Re-fetches `pygame.time.get_ticks()` for the start time, clears boolean pause flags, and delegates the board reset to `self.game.table.handle_start_game()`.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Initiates the 15-second countdown period for the specified player to make their SET selection.
        Parameters:
        player: Identifier (usually integer 1 or 2) representing the player who claimed the turn.
        Limitations:
        -
        Structures:
        Assigns the player parameter to `self.active_player` and records the current millisecond timestamp using `pygame.time.get_ticks()`.
        Outputs:
        None.
        '''
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()

    def clear_set_timer(self):
        '''
        Description:
        Terminates the active answer period and resets the player turn state.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Nullifies `self.active_player` and resets `self.set_start_time` to 0.
        Outputs:
        None.
        '''
        self.active_player = None
        self.set_start_time = 0

    def get_time_left(self):
        '''
        Description:
        Calculates the remaining time for the active player's 15-second SET timer. If the time expires, it penalizes the player, clears their card selections, and displays a timeout message.
        Parameters:
        None.
        Limitations:
        Contains hardcoded logic checking `self.game.current_screen` to differentiate between Multiplayer and Singleplayer scoring.
        Structures:
        Computes elapsed time. If remaining time falls to or below 0, modifies player/computer scores directly based on `self.game.point_loss`, plays a sound, and calls `clear_set_timer()`.
        Outputs:
        Returns the remaining time in seconds (int). Returns 15 if no player is active. Returns 0 if time has expired.
        '''
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
        '''
        Description:
        Calculates the remaining time for the overall game duration, properly accounting for periods when the game is paused.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Subtracts the elapsed active game time from `self.game_duration`. Freezes the calculation at `self.pause_start_time` if the game is currently paused.
        Outputs:
        Returns the remaining game time in seconds (int). Returns 0 if the time has completely expired.
        '''
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
        '''
        Description:
        Pauses the overarching game timer by capturing the exact moment the pause was triggered.
        Parameters:
        None.
        Limitations:
        Only pauses the overall game timer; it does not explicitly halt the 15-second SET timer.
        Structures:
        Updates `self.paused` boolean to True and captures `pygame.time.get_ticks()` into `self.pause_start_time`.
        Outputs:
        None.
        '''
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()

    def resume_game_timer(self):
        '''
        Description:
        Resumes the overall game timer, adjusting the original start time to offset the duration spent in the paused state.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Calculates the difference between current ticks and `self.pause_start_time`, then shifts `self.game_start_time` forward by that exact amount. Reverts `self.paused` to False.
        Outputs:
        None.
        '''
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += paused_duration
            self.paused = False

    def show_message(self, text, duration=1500):
        '''
        Description:
        Assigns a temporary status message to be displayed on the screen's message panel for a defined lifespan.
        Parameters:
        text (str): The string message to display.
        duration (int, optional): The lifespan of the message in milliseconds. Defaults to 1500.
        Limitations:
        Calling this method immediately overwrites any currently displaying message.
        Structures:
        Updates the `self.status_message` string and establishes `self.message_end_time` by adding the duration to current ticks.
        Outputs:
        None.
        '''
        self.status_message = text
        self.message_end_time = pygame.time.get_ticks() + duration