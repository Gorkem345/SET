import pygame
import sys
from utils.constants import WHITE, LIGHT, DARK, BG
from screens.screen import Screen

pygame.init()


class StartScreen(Screen):
    """
    README - StartScreen

    Description:
    This class represents the main menu of the SET game.
    It allows the player to navigate to singleplayer, multiplayer,
    rules, settings, or quit the game.

    Parameters:
    game:
        The main Game object used to control screen transitions
        and shared game resources.

    Structure:
        - Inherits from Screen
        - Loads the game logo image
        - Creates button areas for menu navigation
        - Handles mouse input for screen changes
        - Draws the main menu interface

    Output:
        Displays the start menu and updates the current screen
        based on the player's menu selection.
    """
    def __init__(self, game):
        """Initialize the start screen layout, logo, and menu buttons."""
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
        """
        Description:
        Handles user input on the main menu screen.

        Function:
        Detects mouse clicks on menu buttons and changes the current
        screen accordingly, including starting singleplayer or multiplayer,
        opening rules or settings, or quitting the application.
        """
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
        """Draw the main menu interface, buttons, title, and logo."""
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