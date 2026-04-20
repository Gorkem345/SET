import pygame
from utils.constants import WHITE, DARK, LIGHT


class ConfirmScreen:
    def __init__(self, game):
        self.game = game

        self.yes_button = pygame.Rect(0, 0, 140, 60)

        self.pending_action = None   # "menu" or "restart"
        self.start_time = 0
        self.duration = 3000   # 3 seconds

    def open(self, action):
        self.pending_action = action
        self.start_time = pygame.time.get_ticks()

    def get_seconds_left(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.start_time
        remaining = self.duration - elapsed

        if remaining <= 0:
            return 0

        return remaining // 1000 + 1

    def execute_action(self):
        self.game.game_screen.resume_game_timer()

        if self.pending_action == "menu":
            self.game.game_screen.reset_game_screen()
            self.game.current_screen = self.game.start_screen

        elif self.pending_action == "restart":
            self.game.game_screen.reset_game_screen()
            self.game.current_screen = self.game.game_screen

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.yes_button.collidepoint(mouse):
                self.game.game_screen.resume()
                self.execute_action()

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        # dark overlay
        overlay = pygame.Surface((1080, 720))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # panel
        panel = pygame.Rect(290, 180, 500, 300)
        pygame.draw.rect(screen, (44, 44, 62), panel, border_radius=16)
        pygame.draw.rect(screen, WHITE, panel, 2, border_radius=16)

        if self.pending_action == "menu":
            msg = "Are you sure to go back to menu?"
        else:
            msg = "Are you sure to restart?"

        seconds_left = self.get_seconds_left()

        # countdown finished -> continue game automatically
        if seconds_left == 0:
            self.game.game_screen.resume_game_timer()
            self.game.current_screen = self.game.game_screen
            return

        title_text = self.game.sub_font.render(msg, True, WHITE)
        count_text = self.game.title_font.render(str(seconds_left), True, WHITE)
        info_text = self.game.small_font.render("Click YES to confirm", True, WHITE)

        screen.blit(title_text, title_text.get_rect(center=(panel.centerx, panel.y + 70)))
        screen.blit(count_text, count_text.get_rect(center=(panel.centerx, panel.y + 145)))
        screen.blit(info_text, info_text.get_rect(center=(panel.centerx, panel.y + 200)))

        # yes button
        self.yes_button.center = (panel.centerx, panel.y + 255)
        pygame.draw.rect(
            screen,
            LIGHT if self.yes_button.collidepoint(mouse) else DARK,
            self.yes_button,
            border_radius=12
        )

        yes_text = self.game.small_font.render("YES", True, WHITE)
        screen.blit(yes_text, yes_text.get_rect(center=self.yes_button.center))