import pygame
from utils.constants import WHITE, LIGHT, DARK, BG
from screens.screen import Screen


class RulesScreen(Screen):
    '''
    Description:
    Displays the instructional manual, gameplay mechanics, and winning conditions for the SET game. It renders an array of text lines, presents graphical examples of valid sets, and provides a navigational button to return to the main menu.
    Parameters:
    game: The central Game object acting as the main controller.
    Limitations:
    Text wrapping is not dynamic; the rules are hardcoded into a list of strings and line breaks are handled manually.
    Structures:
    Inherits from the `Screen` base class. Employs a string list for bulk text rendering, `pygame.Rect` for button collision, and `pygame.image.load` for external graphical assets.
    Outputs:
    An initialized RulesScreen instance ready to render the tutorial interface.
    '''
    def __init__(self, game):
        '''
        Description:
        Initializes the Rules screen by loading the text content into an array, defining the "Go back" button's spatial boundaries, instantiating the specific font for the rules, and loading the visual examples sprite.
        Parameters:
        game: The main Game object.
        Limitations:
        Assumes the system has the "Corbel" font installed. Will result in a fatal error if the image path "images/example_sets.png" is incorrect or missing.
        Structures:
        Calls `super().__init__(game)`. Stores text inside the `self.rules` list and creates a `pygame.Rect` positioned in the bottom right corner.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Processes user inputs on the Rules screen, explicitly listening for mouse clicks on the "Go back" button to route the user back to the main menu.
        Parameters:
        event (pygame.event.Event): The Pygame event object triggered by user actions.
        Limitations:
        -
        Structures:
        Evaluates `if event.type == pygame.MOUSEBUTTONDOWN`. Checks mouse collision against `self.goback_button` using `collidepoint()`. Modifies `self.game.current_screen` to trigger the transition.
        Outputs:
        None.
        '''
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.goback_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
        '''
        Description:
        Renders the complete instructional interface. Paints the background, iteratively draws the list of rule strings line-by-line, layers the graphical example image, and draws the interactive "Go back" button with hover color feedback.
        Parameters:
        screen (pygame.Surface): The primary display surface window where graphics are blitted.
        Limitations:
        Text vertical placement relies on a hardcoded absolute Y-coordinate increment (`y += 35`), which could overlap or overflow if additional rules are appended without adjusting the starting coordinate.
        Structures:
        Uses a standard `for loop` to iterate over `self.rules` and sequentially `screen.blit()` each generated text surface. Utilizes inline ternary logic (`LIGHT if ... else DARK`) to dynamically change button colors on mouse hover.
        Outputs:
        Mutates the passed screen surface to reflect the tutorials and UI elements.
        '''
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