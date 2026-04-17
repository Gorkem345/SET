import pygame
from utils.set_table import Table
import utils.image_dictionary as dict

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
        card = pygame.transform.scale(card, (coords[2] * 1.1, coords[3] * 1.1))
        # Rotate 90 degrees
        card = pygame.transform.rotate(card, 90)
        return card

class Display_board:
    def __init__(self, game):
        self.game = game
        self.table = self.game.table
        self.display_card = game.display_card

        # Grid settings
        self.cols = 4
        self.rows = 3

        self.start_x = 400
        self.start_y = 70

        self.spacing_x = 150
        self.spacing_y = 200

    #Detect which card was clicked
    def get_clicked_card_index(self, mouse_pos):
        for index in range(12):
            if self.table.cards_on_table[index] is None:
                continue

            row = index // self.cols
            col = index % self.cols

            x = self.start_x + col * self.spacing_x
            y = self.start_y + row * self.spacing_y

            # Grab the image to know its exact width and height
            card_id = self.table.cards_on_table[index].get_id()
            card_image = self.display_card.get_card_image(card_id)

            # Create a virtual rectangle representing the card's position on screen
            card_rect = pygame.Rect(x, y, card_image.get_width(), card_image.get_height())

            # Check if the mouse click is inside this rectangle
            if card_rect.collidepoint(mouse_pos):
                return index

        return None  # Returned if they clicked empty table space

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

            # Draw Highlight
            # Check if this specific card's index is in the selected list
            if index in self.table.selected:
                # Create a rectangle slightly larger than the card
                highlight_rect = pygame.Rect(x - 5, y - 5, card_image.get_width() + 10, card_image.get_height() + 10)
                # Draw a bright yellow rounded box
                pygame.draw.rect(screen, (255, 230, 0), highlight_rect, border_radius=8)
                # Draw a darker orange border around it to make it pop
                pygame.draw.rect(screen, (255, 150, 0), highlight_rect, width=3, border_radius=8)

            screen.blit(card_image, (x, y))