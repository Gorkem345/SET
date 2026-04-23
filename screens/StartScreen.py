import pygame
import sys
from utils.constants import WHITE, LIGHT, DARK, BG
from screens.screen import Screen

pygame.init()


class StartScreen(Screen):
    '''
    Description:
    Represents the main menu (landing page) of the SET game. It acts as the primary navigation hub, allowing the user to route to the single-player or multiplayer game modes (via the PreStartScreen), view the rules, adjust settings, or quit the application entirely.
    Parameters:
    game: The central Game object acting as the main controller.
    Limitations:
    UI coordinates and layout are hardcoded based on an assumed 1080x720 base resolution. Keyboard navigation (e.g., using arrow keys or Tab) is not supported.
    Structures:
    Inherits from the `Screen` base class. Employs `pygame.image.load` for visual assets and `pygame.Rect` objects to define the clickable hit-boxes for menu buttons.
    Outputs:
    An initialized StartScreen instance ready to capture menu interactions.
    '''
    def __init__(self, game):
        '''
        Description:
        Initializes the StartScreen by loading the game's logo and defining the spatial boundaries (Rects) for all navigation buttons on the screen.
        Parameters:
        game: The main Game object.
        Limitations:
        Assumes the logo image exists at the specific relative path `"images/set_cards.png"`. If missing, the application will crash.
        Structures:
        Calls `super().__init__(game)` to inherit the central controller. Instantiates multiple `pygame.Rect` objects with hardcoded coordinates for hit-box detection.
        Outputs:
        None.
        '''
        super().__init__(game) # store the Game object inside this Startscreen
        # because it needs Game, the main controller to run

        self.logo = pygame.image.load("images/set_cards.png").convert_alpha()
        # Rectangle of button
        self.singleplayer_button = pygame.Rect(440, 310, 200, 80)
        self.play_button = pygame.Rect(440, 410, 200, 80)
        self.quit_button = pygame.Rect(440, 510, 200, 50)

        # Bottom left
        self.rules_button = pygame.Rect(0, 600, 140, 50)
        # Settings Button (Bottom right)
        self.settings_button = pygame.Rect(940, 600, 140, 50)

    def handle_event(self, event):
        '''
        Description:
        Processes user inputs on the main menu, specifically listening for left mouse clicks. Maps clicks on specific button boundaries to screen transitions or application termination.
        Parameters:
        event (pygame.event.Event): The input event captured by the main Pygame event loop.
        Limitations:
        -
        Structures:
        Evaluates `if event.type == pygame.MOUSEBUTTONDOWN`. Uses `pygame.Rect.collidepoint()` to check the mouse position against button Rects. Mutates the central `self.game.current_screen` to trigger transitions, or calls `sys.exit()` to terminate.
        Outputs:
        None.
        '''
        mouse = pygame.mouse.get_pos()  # get mouse position

        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse was clicked
            # If they click SINGLEPLAYER
            if self.singleplayer_button.collidepoint(mouse):
                # Tell the controls screen where to go
                self.game.pre_start_screen.next_screen = self.game.singleplayer_screen
                # Send them to the controls screen
                self.game.current_screen = self.game.pre_start_screen

            # If they click MULTIPLAYER
            elif self.play_button.collidepoint(mouse):
                # Tell the controls screen where to go
                self.game.pre_start_screen.next_screen = self.game.game_screen
                # Send them to the controls screen
                self.game.current_screen = self.game.pre_start_screen

            # Click on Quit --> shut down
            elif self.quit_button.collidepoint(mouse):
                pygame.quit()
                sys.exit()

            # Click on Rules --> go to RulesScreen
            elif self.rules_button.collidepoint(mouse):
                self.game.current_screen = self.game.rules_screen

            # Click on Settings --> go to SettingsScreen
            elif self.settings_button.collidepoint(mouse):
                self.game.current_screen = self.game.settings_screen

    def draw(self, screen):
        '''
        Description:
        Renders the entire main menu interface. Draws the background, the centered logo, the title text, and all navigation buttons. Provides dynamic visual feedback by altering button colors when hovered over by the mouse.
        Parameters:
        screen (pygame.Surface): The primary display surface window where graphics are blitted.
        Limitations:
        -
        Structures:
        Uses `screen.fill()` for the base background. Draws buttons using `pygame.draw.rect()` with a ternary operator (`LIGHT if ... else DARK`) to handle hover states. Uses `screen.blit()` to layer pre-rendered font surfaces and the logo image onto the screen.
        Outputs:
        Refreshes the menu visuals on the provided screen Surface.
        '''
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        title_text = self.game.title_font.render("Welcome to the game Set", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)

        # Buttons: Play, Quit, Rules, Settings
        pygame.draw.rect(screen, LIGHT if self.singleplayer_button.collidepoint(mouse) else DARK,
                         self.singleplayer_button)
        pygame.draw.rect(screen, LIGHT if self.play_button.collidepoint(mouse) else DARK, self.play_button)
        # pygame.draw.rect(screen, color, rectangle) draw rectangle
        # self.play_button.collidepoint(mouse) check hover
        # LIGHT if inside else DARK mouse on button - light, else dark

        pygame.draw.rect(screen, LIGHT if self.quit_button.collidepoint(mouse) else DARK, self.quit_button)
        pygame.draw.rect(screen, LIGHT if self.rules_button.collidepoint(mouse) else DARK, self.rules_button)
        # Draw Settings Button
        pygame.draw.rect(screen, LIGHT if self.settings_button.collidepoint(mouse) else DARK, self.settings_button)

        # Text in buttons
        singleplayer_text = self.game.font.render("Singleplayer", True, WHITE)
        singleplayer_subtext = self.game.sub_font.render("1 Player", True, WHITE)
        play_text = self.game.font.render("Multiplayer", True, WHITE)
        play_subtext = self.game.sub_font.render("2 Players", True, WHITE)
        quit_text = self.game.font.render("Quit", True, WHITE)
        rules_text = self.game.font.render("Rules", True, WHITE)
        # Settings Text
        settings_text = self.game.font.render("Settings", True, WHITE)

        # Place text of buttons on screen
        screen.blit(singleplayer_text, singleplayer_text.get_rect(
            center=(self.singleplayer_button.centerx, self.singleplayer_button.centery - 15)))
        screen.blit(singleplayer_subtext, singleplayer_subtext.get_rect(
            center=(self.singleplayer_button.centerx, self.singleplayer_button.centery + 20)))
        screen.blit(play_text, play_text.get_rect(center=(self.play_button.centerx, self.play_button.centery - 15)))
        screen.blit(play_subtext,
                    play_subtext.get_rect(center=(self.play_button.centerx, self.play_button.centery + 20)))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
        screen.blit(rules_text, rules_text.get_rect(center=self.rules_button.center))
        # Place Settings Text
        screen.blit(settings_text, settings_text.get_rect(center=self.settings_button.center))

        # Logo
        rect = self.logo.get_rect(center=(1080 // 2, 200))
        screen.blit(self.logo, rect)