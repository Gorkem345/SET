import pygame
import utils.card_deck as dict


class Display_card:
    '''
    Description:
    Responsible for loading the master sprite sheet of all SET cards and dynamically extracting, cropping, scaling, and rotating individual card graphics based on their unique ID coordinates.
    Parameters:
    None.
    Limitations:
    Hardcoded to load specifically from "images/cover.png". Assumes the raw sprites require a 90-degree rotation and specific pixel-cropping to remove messy borders.
    Structures:
    Utilizes Pygame Surface operations, including `subsurface`, `transform.scale`, and `transform.rotate`.
    Outputs:
    An initialized Display_card instance capable of serving individual card surfaces.
    '''
    def __init__(self):
        '''
        Description:
        Loads the main sprite sheet containing all cards and assigns pure white as the color key to render the original card backgrounds as transparent.
        Parameters:
        None.
        Limitations:
        Will throw a fatal error if "images/cover.png" is missing from the directory.
        Structures:
        Uses `pygame.image.load()` and `set_colorkey()`.
        Outputs:
        None.
        '''
        self.sheet = pygame.image.load("images/cover.png").convert()
        self.sheet.set_colorkey((255, 255, 255))

    def get_card_image(self, card_id):
        '''
        Description:
        Retrieves the specific sub-image of a card from the master sprite sheet, trims its edges, scales it up, and rotates it to fit standard playing card dimensions.
        Parameters:
        card_id (str): The 4-character identifier of the requested card (e.g., 'erc1').
        Limitations:
        Relies heavily on the external global dictionary `dict.cards` to provide accurate coordinate data. Crop values (8px) and scaling factors (1.2x) are hardcoded.
        Structures:
        Constructs a new `pygame.Rect` to isolate the target area. Uses Pygame subsurface extraction and transformation modules.
        Outputs:
        Returns a formatted `pygame.Surface` representing the finalized, individual card image.
        '''
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
    '''
    Description:
    Manages the visual layout and rendering of the 12 playing cards on the table. It handles translating the 1D card data into a 2D grid display, drawing dynamic selection/hint borders, and translating physical mouse clicks back into logical board indices.
    Parameters:
    game: The central Game object controller.
    Limitations:
    The grid configuration (4 columns x 3 rows) and spatial pixel intervals are hardcoded and heavily tailored for a 1080x720 window layout.
    Structures:
    Maintains direct references to `game.table` and `game.display_card`. Employs iteration and modulo arithmetic for grid placements.
    Outputs:
    An initialized Display_board object ready to be drawn on the active screen.
    '''
    def __init__(self, game):
        '''
        Description:
        Initializes the board references and defines the geometric parameters (columns, rows, starting X/Y, and spacing) for the 12-card grid layout.
        Parameters:
        game: The main Game controller object.
        Limitations:
        -
        Structures:
        Binds references to the table logic and card display modules.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Determines which specific card slot was clicked by mapping the provided mouse coordinates against the calculated geometric boundaries of each active card on the table.
        Parameters:
        mouse_pos (tuple): The (x, y) coordinate pair representing the user's mouse click.
        Limitations:
        Card hit-box width (120) and height (185) are hardcoded.
        Structures:
        Loops through valid table indices using integer division (`//`) and modulo (`%`) to calculate individual 2D screen positions. Evaluates collisions via `pygame.Rect.collidepoint()`.
        Outputs:
        Returns an integer (0-11) representing the index of the clicked card, or `None` if the click landed on an empty space.
        '''
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
        '''
        Description:
        Renders the entire card grid onto the screen. This involves drawing the dynamic, colored highlight borders (yellow for selected, cyan for hinted), creating clean white background cards, and precisely centering the cropped card graphics on top.
        Parameters:
        screen (pygame.Surface): The primary Pygame display surface where the board will be rendered.
        Limitations:
        Visual styling (colors, padding offsets, border radii) are entirely hardcoded.
        Structures:
        Uses `enumerate()` to iterate through table cards. Draws geometric background and border shapes using `pygame.draw.rect()` and layers the final card graphic via `screen.blit()`.
        Outputs:
        Mutates the passed screen surface to reflect the current physical state of the game board.
        '''
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