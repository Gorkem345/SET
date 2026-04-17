import pygame
from set_table import Table
from image_dictionary import Card

class Display_card:
    def __init__(self):
        self.sheet = pygame.image.load("images/cover.png").convert()
        # Make white invisible
        #self.sheet.set_colorkey((255, 255, 255))

    def get_card_image(self, card_id):
        coords = dict.cards[card_id].coordinates

        rect = pygame.Rect(coords[0], coords[1], coords[2], coords[3])
        card = self.sheet.subsurface(rect)
        # Scale
        card = pygame.transform.scale(card, (coords[2] * 2, coords[3] * 2))
        # Rotate 90 degrees
        card = pygame.transform.rotate(card, 90)
        return card

class Display_board:
    def __init__(self, game, Table):
        self.game = game
        self.table = Table()
        self.display_card = game.display_card

        # Grid settings
        self.cols = 4
        self.rows = 3

        self.start_x = 150
        self.start_y = 100

        self.spacing_x = 150
        self.spacing_y = 200

    def draw(self, screen):
        for index, card in enumerate(self.table.cards_on_table):
            if card is None:
                continue
            card_id = card.get_id()

            row = index // self.cols
            col = index % self.cols

            x = self.start_x + col * self.spacing_x
            y = self.start_y + row * self.spacing_y

            card_image = self.display_card.get_card_image(card_id)
            screen.blit(card_image, (x, y))

