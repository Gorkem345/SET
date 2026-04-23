import pygame
from utils.constants import WHITE, LIGHT, DARK, BG
from screens.screen import Screen


class WinnerScreen(Screen):
    """
    README - WinnerScreen

    Description:
    This class displays the final result of the game after it ends.
    It shows the winner, player scores, and provides a button to return to the main menu.

    Parameters:
    game:
        The main Game object used to access scores, winner information,
        and control screen transitions.

    Structure:
        - Inherits from Screen
        - Displays a result panel with game outcome
        - Shows different results for multiplayer and singleplayer
        - Contains a "Back to Menu" button

    Output:
        Displays the final game result and allows the player to return to the menu.
    """

    def __init__(self, game):
        """Initialize result panel and navigation button."""
        super().__init__(game)
        self.prev_screen = None

        # result panel
        self.result_panel = pygame.Rect(290, 120, 500, 320)

        # button
        self.homepage_button = pygame.Rect(420, 480, 240, 60)

    def handle_event(self, event):
        """Handle click event to return to the start screen."""
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.homepage_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
        """
        Description:
        Renders the game over screen with winner and score information.

        Function:
        Displays the result panel, shows the winner and scores depending on
        game mode, and draws a button that allows the player to return to the menu.
        """
        self.game.table.game_end = True
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        # --- result box background ---
        pygame.draw.rect(screen, DARK, self.result_panel, border_radius=18)
        pygame.draw.rect(screen, LIGHT, self.result_panel, 3, border_radius=18)

        # --- title ---
        title_text = self.game.title_font.render("Game Over", True, WHITE)
        screen.blit(
            title_text,
            title_text.get_rect(center=(self.result_panel.centerx, self.result_panel.y + 50))
        )

        # --- winner result ---
        if self.prev_screen == self.game.game_screen:
            lines = [
                f"Winner: {self.game.winner}",
                f"P1 Score: {self.game.p1_score}",
                f"P2 Score: {self.game.p2_score}"
            ]
        elif self.prev_screen == self.game.singleplayer_screen:
            lines = [
                f"Winner: {self.game.winner}",
                f"P1 Score: {self.game.p1_score}",
                f"Computer Score: {self.game.comp_score}"
            ]
        else:
            lines = ["Winner: ---", "P1 Score: ---", "P2 Score: ---"]

        # --- draw result lines ---
        for i, line in enumerate(lines):
            if i == 0:
                text_surface = self.game.title_font.render(line, True, WHITE)
            else:
                text_surface = self.game.sub_font.render(line, True, WHITE)

            text_rect = text_surface.get_rect(
                center=(self.result_panel.centerx, self.result_panel.y + 130 + i * 55)
            )
            screen.blit(text_surface, text_rect)

        # --- button ---
        button_color = LIGHT if self.homepage_button.collidepoint(mouse) else DARK
        pygame.draw.rect(screen, button_color, self.homepage_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.homepage_button, 2, border_radius=12)

        homepage_text = self.game.sub_font.render("Back to Menu", True, WHITE)
        screen.blit(
            homepage_text,
            homepage_text.get_rect(center=self.homepage_button.center)
        )