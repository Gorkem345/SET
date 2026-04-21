import pygame
from utils.constants import WHITE, LIGHT, DARK, BG


class WinnerScreen:
    def __init__(self, game):
        self.game = game
        self.prev_screen = None

        # result panel
        self.result_panel = pygame.Rect(290, 120, 500, 320)

        # button
        self.homepage_button = pygame.Rect(420, 480, 240, 60)

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.homepage_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen

    def draw(self, screen):
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