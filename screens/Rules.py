import pygame
from utils.constants import WHITE, LIGHT, DARK, BG
from screens.screen import Screen


class RulesScreen(Screen):
    def __init__(self, game):
        super().__init__(game)
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
            " or is different on each card.",
            " ",
            "Winning conditions",
            '1. When the timer expires, the player with the highest total score is declared the winner.',
            '2. If the deck is empty and no further sets can be formed, the player with the highest score wins.'
        ]
        # Size and place of button
        self.goback_button = pygame.Rect(940, 600, 140, 50)
        # Font for rules
        self.rules_font = pygame.font.SysFont("Corbel", 20)

        self.examples = pygame.image.load("images/example_sets.png").convert_alpha()

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
        # Example sets image + text
        rect = self.examples.get_rect(center= (880, 340))
        screen.blit(self.examples, rect)
        examples_text = self.game.sub_font.render("Example sets:", True, WHITE)
        examples_rect = examples_text.get_rect(center=(880, 190))
        screen.blit(examples_text, examples_rect)