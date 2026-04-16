import pygame
import image_dictionary
from constants import WHITE

class GameScreen:
    def __init__(self, game):
        self.game = game

        self.sheet = pygame.image.load("images/cover.png").convert()

        id = "srs3"

        self.card_rect = pygame.Rect(
            image_dictionary.cards[id].coordinates[0],
            image_dictionary.cards[id].coordinates[1],
            image_dictionary.cards[id].coordinates[2],
            image_dictionary.cards[id].coordinates[3]
        )

        self.card = self.sheet.subsurface(self.card_rect)

        self.card = pygame.transform.scale(
            self.card,
            (
                image_dictionary.cards[id].coordinates[2] * 2,
                image_dictionary.cards[id].coordinates[3] * 2
            )
        )

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
        screen.fill((40, 40, 40))

        screen.blit(self.card, (0, 0))

        text = self.game.font.render(
            "Game Started! Press ESC to go back.",
            True,
            WHITE
        )
        screen.blit(text, (250, 350))