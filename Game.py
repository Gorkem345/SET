import pygame
import sys
from screens.StartScreen import StartScreen
from screens.Multiplayer import Multiplayer
from screens.Rules import RulesScreen
from screens.WinnerScreen import WinnerScreen
from screens.TableDisplay import Display_card
from screens.settings_screen import SettingsScreen
from utils.set_table import Table
from screens.Singleplayer import SingleplayerScreen
from screens.ConfirmScreen import ConfirmScreen
from screens.PreStartScreen import PreStartScreen


class Game:
    '''
    Description:
    Serves as the central controller and main entry point for the SET game application. It initializes the Pygame
    environment (display, audio, typography), instantiates all modular screen views, and generates the core game
    logic engine (Table). It acts as the ultimate state manager, holding global variables like scores and settings,
    and continuously runs the primary game loop handling inputs, logic updates, and rendering.

    Parameters:
        - None (The class is initialized without external arguments and sets up its default configurations internally).

    Limitations:
        - The application relies on the system having the "Corbel" font installed. If it is missing, Pygame will fall
        back to a default font, which may alter the visual layout.
        - The base resolution is hardcoded to 1080x720. It relies entirely on the pygame.RESIZABLE and pygame.SCALED
        flags to adapt to different monitor sizes.

    Structures:
        - Maintains the central game state and scoring variables: winner, p1_score, p2_score, comp_score, point_gain,
        point_loss, and turn_duration_ms.
        - Holds instantiated objects for every user interface view (e.g., start_screen, singleplayer_screen) and
        dynamically tracks the active view with the current_screen attribute.
        - Encapsulates the core rules and logic of the card game with self.table.
    Outputs:
        - Launches the interactive Pygame window and indefinitely executes the `run()` method's while-loop (Event -> Update -> Draw) until the user triggers a `pygame.QUIT` event.
    '''
    def __init__(self):
        '''
        Description: Initializes the Pygame display, audio mixer, and fonts. Instantiates all modular screens and the
        core game table, and sets default values for the game state, scoring, and timers.
        Parameters: None.
        Limitations: Base window size is hardcoded to 1080x720. Text rendering depends on the system having the
        "Corbel" font.
        Structures: Pygame display surfaces, font objects, custom screen class instances, and basic primitive variables
        (integers/strings) for game state.
        Outputs: A fully configured Game object ready to enter the main loop.
        '''
        self.screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE | pygame.SCALED)
        pygame.mixer.init()

        self.turn_duration_ms = 300000

        #create font type and size
        self.font = pygame.font.SysFont("Corbel", 40)
        self.sub_font = pygame.font.SysFont("Corbel", 25)
        self.title_font = pygame.font.SysFont("Corbel", 60)
        self.small_font = pygame.font.SysFont("Corbel", 18)

        self.display_card = Display_card()
        self.table = Table()
        self.table.handle_start_game()

        #create different screens/pages
        self.start_screen = StartScreen(self)
        self.singleplayer_screen = SingleplayerScreen(self)
        self.game_screen = Multiplayer(self)
        self.rules_screen = RulesScreen(self)
        self.winner_screen = WinnerScreen(self)
        self.confirm_screen = ConfirmScreen(self)
        self.pre_start_screen = PreStartScreen(self)
        self.settings_screen = SettingsScreen(self)

        self.current_screen = self.start_screen
        self.running = True

        #add winner data
        self.winner = ""
        self.p1_score = 0
        self.p2_score = 0
        self.comp_score = 0
        self.point_gain = 1
        self.point_loss = 1

    def run(self):
        '''
        Description: The primary execution loop of the application. It continuously intercepts user inputs, triggers
        backend logic updates (like timers), and commands the active screen to draw itself.
        Parameters: None.
        Limitations: The loop runs indefinitely until a QUIT event is detected. It currently runs as fast as the CPU
        allows, as there is no explicit FPS cap defined here.
        Structures: A continuous while-loop encompassing a Pygame event-handling for-loop, followed by delegated
        update() and draw() method calls.
        Outputs: Refreshes the display hardware every frame and triggers a clean system exit when the window is closed.
        '''
        while self.running:
            # 1. Handle Events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.current_screen.handle_event(event)
            # 2. Update Game Logic
            self.table.update()
            # 3. Draw the Screen
            self.current_screen.draw(self.screen)
            pygame.display.update()
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    Game().run() # Game loop
