import pygame
import utils.card_deck as dict


class Display_card:
    def __init__(self):
        self.sheet = pygame.image.load("images/cover.png").convert()
        self.sheet.set_colorkey((255, 255, 255))

    def get_card_image(self, card_id):
        coords = dict.cards[card_id].coordinates

        # Shave off the messy borders
        crop_x = 8
        crop_y = 8

        rect = pygame.Rect(
            coords[0] + crop_x,
            coords[1] + crop_y,
            coords[2] - (crop_x * 2),
            coords[3] - (crop_y * 2)
        )

        card = self.sheet.subsurface(rect)

        # Scale
        card = pygame.transform.scale(card, (int(rect.width * 1.2), int(rect.height * 1.2)))

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

    def get_clicked_card_index(self, mouse_pos):
        # We need to calculate based on the new white background sizes
        CARD_WIDTH = 120
        CARD_HEIGHT = 185

        for index in range(12):
            if self.table.cards_on_table[index] is None:
                continue

            row = index // self.cols
            col = index % self.cols

            x = self.start_x + col * self.spacing_x
            y = self.start_y + row * self.spacing_y

            # Check collision against the white card background
            card_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

            if card_rect.collidepoint(mouse_pos):
                return index

        return None

    def draw(self, screen):
        # Define the physical size of your playing cards
        CARD_WIDTH = 120
        CARD_HEIGHT = 185

        for index, card in enumerate(self.table.cards_on_table):
            if card is None:
                continue
            card_id = card.get_id()

            row = index // self.cols
            col = index % self.cols

            x = self.start_x + col * self.spacing_x
            y = self.start_y + row * self.spacing_y

            card_image = self.display_card.get_card_image(card_id)
            bg_rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)

            # --- HIGHLIGHTS ---
            # 1. Selected highlight (Yellow)
            if index in self.table.selected:
                highlight_rect = pygame.Rect(x - 5, y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                pygame.draw.rect(screen, (255, 230, 0), highlight_rect, border_radius=12)
                pygame.draw.rect(screen, (255, 150, 0), highlight_rect, width=3, border_radius=12)

            # 2. Hint highlight (Cyan)
            elif hasattr(self.table, 'hinted') and index in self.table.hinted:
                hint_rect = pygame.Rect(x - 5, y - 5, CARD_WIDTH + 10, CARD_HEIGHT + 10)
                pygame.draw.rect(screen, (0, 255, 255), hint_rect, border_radius=12)
                pygame.draw.rect(screen, (0, 150, 255), hint_rect, width=3, border_radius=12)

            else:
                # Subtle dark border if not highlighted
                pygame.draw.rect(screen, (100, 100, 100), bg_rect, width=2, border_radius=10)

            # Draw the perfect white card background (this goes ON TOP of the highlight so the highlight looks like a border!)
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, border_radius=10)

            # Center the shape inside the white card
            img_x = x + (CARD_WIDTH - card_image.get_width()) // 2
            img_y = y + (CARD_HEIGHT - card_image.get_height()) // 2

            screen.blit(card_image, (img_x, img_y))