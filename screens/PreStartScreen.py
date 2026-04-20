import pygame
from utils.constants import WHITE, DARK, LIGHT


class PreStartScreen:
    def __init__(self, game):
        self.game = game

        # The target screen we will go to after pressing Continue
        # (This will be either singleplayer_screen or game_screen)
        self.next_screen = None

        # Continue Button at the middle bottom
        self.continue_button = pygame.Rect(0, 0, 240, 60)
        self.continue_button.center = (540, 640)  # 540 is middle of 1080 width

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.continue_button.collidepoint(mouse):

                # 1. Reset the deck and table!
                self.game.table.handle_start_game()

                # 2. Reset the specific game screen's scores and timers
                if hasattr(self.next_screen, 'reset_game_screen'):
                    self.next_screen.reset_game_screen()

                # 3. Transition to the game!
                self.game.current_screen = self.next_screen

    def draw(self, screen):
        # Dark slate background
        screen.fill((44, 44, 62))
        mouse = pygame.mouse.get_pos()

        # --- TITLE ---
        title_text = self.game.title_font.render("How to Play", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(540, 80)))

        # --- INSTRUCTIONS ---
        instructions = [
            "1. Find 3 cards that form a SET.",
            "2. A SET is formed when for each of the 4 features (Color, Shape, Filling, Count),",
            "   the features are either ALL THE SAME or ALL DIFFERENT.",
            "3. Hit your player's key to lock in your turn, then click 3 cards before time runs out!"
        ]

        start_y = 160
        for line in instructions:
            text = self.game.sub_font.render(line, True, WHITE)
            screen.blit(text, (80, start_y))
            start_y += 40

        # --- DRAW VISUAL CONTROLS ---

        # 1. SPACEBAR (Player 1)
        pygame.draw.rect(screen, WHITE, (150, 400, 240, 60), border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), (150, 400, 240, 60), width=4, border_radius=8)
        space_text = self.game.sub_font.render("SPACEBAR", True, DARK)
        screen.blit(space_text, space_text.get_rect(center=(270, 430)))

        p1_text = self.game.sub_font.render("Player 1 Call SET", True, WHITE)
        screen.blit(p1_text, p1_text.get_rect(center=(270, 490)))

        # 2. MOUSE (Selection)
        # Draw the mouse body
        pygame.draw.rect(screen, WHITE, (490, 370, 100, 140), border_radius=40)
        # Draw the mouse buttons/wheel lines
        pygame.draw.line(screen, DARK, (540, 370), (540, 430), 4)
        pygame.draw.line(screen, DARK, (490, 430), (590, 430), 4)

        mouse_text = self.game.sub_font.render("Left Click", True, WHITE)
        screen.blit(mouse_text, mouse_text.get_rect(center=(540, 540)))
        select_text = self.game.sub_font.render("Select Cards", True, WHITE)
        screen.blit(select_text, select_text.get_rect(center=(540, 570)))

        # 3. ENTER KEY (Player 2)
        pygame.draw.rect(screen, WHITE, (690, 400, 160, 60), border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), (690, 400, 160, 60), width=4, border_radius=8)
        enter_text = self.game.sub_font.render("ENTER", True, DARK)
        screen.blit(enter_text, enter_text.get_rect(center=(770, 430)))

        p2_text = self.game.sub_font.render("Player 2 Call SET", True, WHITE)
        screen.blit(p2_text, p2_text.get_rect(center=(770, 490)))

        # --- CONTINUE BUTTON ---
        pygame.draw.rect(
            screen,
            LIGHT if self.continue_button.collidepoint(mouse) else DARK,
            self.continue_button,
            border_radius=12
        )
        pygame.draw.rect(screen, WHITE, self.continue_button, width=2, border_radius=12)

        cont_text = self.game.font.render("CONTINUE", True, WHITE)
        screen.blit(cont_text, cont_text.get_rect(center=self.continue_button.center))