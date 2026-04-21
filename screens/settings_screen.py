import pygame
from utils.constants import WHITE, DARK, LIGHT, BLUE
from screens.screen import Screen


class SettingsScreen(Screen):
    def __init__(self, game):
        super().__init__(game)

        self.game = game

        # Default settings ### Keep as strings
        self.text_duration = "5"
        self.text_gain = "1"
        self.text_loss = "1"

        self.active_field = None

        # LAYOUT COORDINATES
        # The center X coordinate for the input boxes (buttons)
        box_center_x = 475

        self.rect_duration = pygame.Rect(0, 0, 100, 50)
        self.rect_duration.center = (box_center_x, 220)

        self.rect_gain = pygame.Rect(0, 0, 100, 50)
        self.rect_gain.center = (box_center_x, 360)

        self.rect_loss = pygame.Rect(0, 0, 100, 50)
        self.rect_loss.center = (box_center_x, 500)

        # SAVE BUTTON (Aligned to the left margin at x=100)
        self.save_button = pygame.Rect(0, 0, 260, 60)
        self.save_button.center = (540, 630)

    def save_and_exit(self):
        # If left empty assign the default values
        if self.text_duration == "" or int(self.text_duration) < 1:
            self.text_duration = "5"

        if self.text_gain == "": self.text_gain = "1"
        if self.text_loss == "": self.text_loss = "1"

        # Record in self.game
        self.game.turn_duration_ms = int(self.text_duration) * 1000 * 60
        self.game.point_gain = int(self.text_gain)
        self.game.point_loss = int(self.text_loss)

        # Go back to StartScreen
        self.game.current_screen = self.game.start_screen

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.rect_duration.collidepoint(mouse):
                    self.active_field = 'duration'
                    self.text_duration = ""
                elif self.rect_gain.collidepoint(mouse):
                    self.active_field = 'gain'
                    self.text_gain = ""
                elif self.rect_loss.collidepoint(mouse):
                    self.active_field = 'loss'
                    self.text_loss = ""
                else:
                    self.active_field = None  # Remove the selection when pressed somewhere else

                # Pressed the save button
                if self.save_button.collidepoint(mouse):
                    self.save_and_exit()

        elif event.type == pygame.KEYDOWN:
            if self.active_field is not None:

                if event.key == pygame.K_BACKSPACE:
                    if self.active_field == 'duration':
                        self.text_duration = self.text_duration[:-1]
                    elif self.active_field == 'gain':
                        self.text_gain = self.text_gain[:-1]
                    elif self.active_field == 'loss':
                        self.text_loss = self.text_loss[:-1]

                # Can only type numeric characters
                elif event.unicode.isnumeric():
                    char = event.unicode

                    if self.active_field == 'duration':
                        yeni_metin = self.text_duration + char
                        # Max 20 minutes
                        if int(yeni_metin) > 20:
                            self.text_duration = "20"
                        else:
                            self.text_duration = yeni_metin

                    elif self.active_field == 'gain':
                        yeni_metin = self.text_gain + char
                        # Max 10 points can be gained
                        if int(yeni_metin) > 10:
                            self.text_gain = "10"
                        else:
                            self.text_gain = yeni_metin

                    elif self.active_field == 'loss':
                        yeni_metin = self.text_loss + char
                        # Max 10 points can be lost
                        if int(yeni_metin) > 10:
                            self.text_loss = "10"
                        else:
                            self.text_loss = yeni_metin

    def draw(self, screen):
        screen.fill((44, 44, 62))
        mouse = pygame.mouse.get_pos()

        # Header (Kept centered at the top)
        title_text = self.game.title_font.render("Settings", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(540, 80)))

        def draw_input_section(rect, label_text, value_text, is_active):
            # Label - Now pinned to the left margin (X=100) and vertically centered with the box
            label = self.game.sub_font.render(label_text, True, BLUE)
            screen.blit(label, label.get_rect(midleft=(100, rect.centery)))

            # The box
            box_color = LIGHT if is_active else DARK
            pygame.draw.rect(screen, box_color, rect, border_radius=12)

            # Add border when selected
            if is_active:
                pygame.draw.rect(screen, (0, 255, 255), rect, width=3, border_radius=12)
            else:
                pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=12)

            # Value rendered inside the box
            val_surf = self.game.font.render(value_text, True, WHITE)
            screen.blit(val_surf, val_surf.get_rect(center=rect.center))

        # Draw the inputs side-by-side
        draw_input_section(self.rect_duration, "Game Duration (Minutes) [1-20]", self.text_duration,
                           self.active_field == 'duration')
        draw_input_section(self.rect_gain, "Points Earned [0-10]", self.text_gain, self.active_field == 'gain')
        draw_input_section(self.rect_loss, "Points Lost [0-10]", self.text_loss, self.active_field == 'loss')

        # Save and exit button
        btn_color = LIGHT if self.save_button.collidepoint(mouse) else DARK
        pygame.draw.rect(screen, btn_color, self.save_button, border_radius=12)
        pygame.draw.rect(screen, WHITE, self.save_button, width=2, border_radius=12)

        btn_text = self.game.font.render("SAVE AND EXIT", True, WHITE)
        screen.blit(btn_text, btn_text.get_rect(center=self.save_button.center))