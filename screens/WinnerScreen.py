import pygame
from utils.constants import WHITE, LIGHT, DARK, BG

class WinnerScreen:
    def __init__(self, game):
        self.game = game #this is a genius idea to connect to the Game object
        self.homepage_button = pygame.Rect(470, 410, 140, 50)

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN: #if mouse was clicked
            if self.homepage_button.collidepoint(mouse):
                self.game.current_screen = self.game.start_screen


    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        homepage_text = self.game.sub_font.render("Back to menu", True, WHITE)

        pygame.draw.rect(screen, LIGHT if self.homepage_button.collidepoint(
            mouse) else DARK, self.homepage_button)
        #Draw the button rectangle

        screen.blit(homepage_text,homepage_text.get_rect(center=self.homepage_button.center))
        #put the text inside the text rect, at center


        #Winner result
        lines = [
            f"Winner: {self.game.winner}",
            f"P1 score: {self.game.p1_score}",
            f"P2 score: {self.game.p2_score}"
        ]

        # Draw each line
        for i, line in enumerate(lines):
            text_surface = self.game.title_font.render(line, True, WHITE)

            text_rect = text_surface.get_rect(
                center=(1080 // 2, 80 + i * 60)  # move each line down
            )
            screen.blit(text_surface, text_rect)

