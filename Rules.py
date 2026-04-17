import pygame
import sys
from constants import WHITE, LIGHT, DARK, BG

class RulesScreen:
    def __init__(self, game):
        self.game = game
        #self.logo = pygame.image.load("set_cards.png").convert_alpha() --> other images?
        self.rules = [
            "Goal: Find a 'Set' of 3 cards from 12 cards displayed on the screen.",
            "A set must satisfy specific rules.",
            "",
            "Each card has 4 attributes:",
            "- Color: red, green, or purple",
            "- Shape: oval, squiggle, or diamond",
            "- Number: one, two, or three symbols",
            "- Shading: solid, open, or striped",
            " ",
            "A 'Set' consists of three cards in which each attribute is EITHER the same",
            "on each card OR is different on each card.",
            "That is to say, any attribute in the 'Set' of three cards is either common to all three cards",
            " or is different on each card."
        ]
        # Size and place of button
        self.goback_button = pygame.Rect(0, 600, 140, 50)
        # Font for rules
        self.rules_font = pygame.font.SysFont("Corbel", 20)

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.goback_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)
        # Title
        title_text = self.game.title_font.render("How to play Set:", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)
        # Go back button --> goes back to StartScreen
        pygame.draw.rect(screen, LIGHT if self.goback_button.collidepoint(mouse) else DARK, self.goback_button)
        goback_text = self.game.font.render("Go back", True, WHITE)
        screen.blit(goback_text, goback_text.get_rect(center=self.goback_button.center))

        y = 120
        for line in self.rules:
            surf = self.rules_font.render(line, True, WHITE)
            screen.blit(surf, (100, y))
            y += 35