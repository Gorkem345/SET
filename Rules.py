import pygame
import sys
from constants import WHITE, LIGHT, DARK, BG

class RulesScreen:
    def __init__(self, game):
        self.game = game
        #self.logo = pygame.image.load("set_cards.png").convert_alpha() --> other images?
        # Size and place of button
        self.goback_button = pygame.Rect(0, 600, 140, 50)

    #text with explanation
    #button to go back to startscreen

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.goback_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        title_text = self.game.title_font.render("These are the rules:", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)

        pygame.draw.rect(screen, LIGHT if self.goback_button.collidepoint(mouse) else DARK, self.goback_button)

        goback_text = self.game.font.render("Go back", True, WHITE)

        screen.blit(goback_text, goback_text.get_rect(center=self.goback_button.center))