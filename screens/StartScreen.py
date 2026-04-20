import pygame
import sys
from utils.constants import WHITE, LIGHT, DARK, BG

pygame.init()

class StartScreen:
    def __init__(self, game):
        self.game = game #store the Game object inside this Startscreen
                         #because it needs Game, the main controller to run

        self.logo = pygame.image.load("images/set_cards.png").convert_alpha()
        # Rectangle of button
        self.singleplayer_button = pygame.Rect(440, 310, 200, 80)
        self.play_button = pygame.Rect(440, 410, 200, 80)
        self.quit_button = pygame.Rect(440, 510, 200, 50)
        self.rules_button = pygame.Rect(0, 600, 140, 50)

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos() #get mouse position

        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse was clicked
            # Click on Singleplayer --> go to SingleplayerScreen
            if self.singleplayer_button.collidepoint(mouse):  # if the mouse is clicked inside the play button area
                self.game.current_screen = self.game.singleplayer_screen
            # Click on Play --> go to GameScreen
            elif self.play_button.collidepoint(mouse): #if the mouse is clicked inside the play button area
                self.game.game_screen.reset_game_screen() #connect to Game, use game_screen object to connect Gamescreen,
                                                          # call the reset game screen function
                self.game.current_screen = self.game.game_screen
            # Click on Quit --> shut down
            elif self.quit_button.collidepoint(mouse):
                pygame.quit()
                sys.exit()
            # Click on Rules --> go to RulesScreen
            elif self.rules_button.collidepoint(mouse):
                self.game.current_screen = self.game.rules_screen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        title_text = self.game.title_font.render("Welcome to the game Set", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)

        # Buttons: Play, Quit, Rules
        pygame.draw.rect(screen, LIGHT if self.singleplayer_button.collidepoint(mouse) else DARK, self.singleplayer_button)
        pygame.draw.rect(screen, LIGHT if self.play_button.collidepoint(mouse) else DARK, self.play_button)
        #pygame.draw.rect(screen, color, rectangle) draw rectangle
        #self.play_button.collidepoint(mouse) check hover
        #LIGHT if inside else DARK mouse on button - light, else dark

        pygame.draw.rect(screen, LIGHT if self.quit_button.collidepoint(mouse) else DARK, self.quit_button)
        pygame.draw.rect(screen, LIGHT if self.rules_button.collidepoint(mouse) else DARK, self.rules_button)

        # Text in buttons
        singleplayer_text = self.game.font.render("Singleplayer", True, WHITE)
        singleplayer_subtext = self.game.sub_font.render("1 Player", True, WHITE)
        play_text = self.game.font.render("Multiplayer", True, WHITE)
        play_subtext = self.game.sub_font.render("2 Players", True, WHITE)
        quit_text = self.game.font.render("Quit", True, WHITE)
        rules_text = self.game.font.render("Rules", True, WHITE)

        # Place text of buttons on screen
        screen.blit(singleplayer_text, singleplayer_text.get_rect(center=(self.singleplayer_button.centerx, self.singleplayer_button.centery - 15)))
        screen.blit(singleplayer_subtext, singleplayer_subtext.get_rect(center=(self.singleplayer_button.centerx, self.singleplayer_button.centery + 20)))
        screen.blit(play_text, play_text.get_rect(center=(self.play_button.centerx, self.play_button.centery - 15)))
        screen.blit(play_subtext, play_subtext.get_rect(center=(self.play_button.centerx, self.play_button.centery + 20)))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
        screen.blit(rules_text, rules_text.get_rect(center=self.rules_button.center))

        # Logo
        rect = self.logo.get_rect(center=(1080 // 2, 200))
        screen.blit(self.logo, rect)

