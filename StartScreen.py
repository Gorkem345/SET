import pygame
import sys
from constants import WHITE, LIGHT, DARK, BG

pygame.init()

class StartScreen:
    def __init__(self, game):
        self.game = game
        self.logo = pygame.image.load("set_cards.png").convert_alpha()

        self.play_button = pygame.Rect(470, 310, 140, 80)
        self.quit_button = pygame.Rect(470, 410, 140, 50)
        self.rules_button = pygame.Rect(0, 600, 140, 50)

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button.collidepoint(mouse):
                print("Game Screen")
                self.game.current_screen = self.game.game_screen

            if self.quit_button.collidepoint(mouse):
                pygame.quit()
                sys.exit()

            if self.rules_button.collidepoint(mouse):
                print("Rules") ##Replace with RulesScreen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        title_text = self.game.title_font.render("Welcome to the game Set", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)

        #buttons
        pygame.draw.rect(screen, LIGHT if self.play_button.collidepoint(mouse) else DARK, self.play_button)
        pygame.draw.rect(screen, LIGHT if self.quit_button.collidepoint(mouse) else DARK, self.quit_button)
        pygame.draw.rect(screen, LIGHT if self.rules_button.collidepoint(mouse) else DARK, self.rules_button)

        #text
        play_text = self.game.font.render("Play", True, WHITE)
        play_subtext = self.game.sub_font.render("2 Players", True, WHITE)
        quit_text = self.game.font.render("Quit", True, WHITE)
        rules_text = self.game.font.render("Rules", True, WHITE)

        screen.blit(play_text, play_text.get_rect(center=(self.play_button.centerx, self.play_button.centery - 15)))
        screen.blit(play_subtext, play_subtext.get_rect(center=(self.play_button.centerx, self.play_button.centery + 20)))
        screen.blit(quit_text, quit_text.get_rect(center=self.quit_button.center))
        screen.blit(rules_text, rules_text.get_rect(center=self.rules_button.center))

        #logo
        rect = self.logo.get_rect(center=(1080 // 2, 200))
        screen.blit(self.logo, rect)

