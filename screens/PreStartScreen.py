import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.screen import Screen

class PreStartScreen(Screen):
    """
    README - PreStartScreen

    Description:
    This class represents the pre-start screen where players can view controls
    and (for singleplayer) choose the game difficulty before starting.

    Parameters:
    game:
        The main Game object used for accessing screens, table state,
        and difficulty settings.

    Structure:
        - Inherits from Screen
        - Displays control instructions
        - Allows difficulty selection (singleplayer only)
        - Contains a Continue button to start the game

    Output:
        Sets up initial game state (difficulty, table reset) and transitions
        to the selected game screen.
    """
    def __init__(self, game):
        """Initialize control display, difficulty selection, and buttons."""
        super().__init__(game)

        # The target screen we will go to after pressing Continue
        self.next_screen = None

        # --- DIFFICULTY SETUP ---
        self.selected_difficulty = "Normal"
        # Set the default value inside SingleplayerScreen immediately
        self.game.singleplayer_screen.difficulty = "Normal"

        # --- BUTTON RECTS ---
        # Difficulty Buttons (Side-by-side)
        self.easy_button = pygame.Rect(260, 480, 160, 60)
        self.normal_button = pygame.Rect(460, 480, 160, 60)
        self.hard_button = pygame.Rect(660, 480, 160, 60)

        # Continue Button (Middle bottom)
        self.continue_button = pygame.Rect(0, 0, 240, 60)
        self.continue_button.center = (540, 620)  # 540 is middle of 1080 width

    def handle_event(self, event):
        """Handle clicks for difficulty selection and starting the game."""
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # --- DIFFICULTY CLICKS ---
            if self.easy_button.collidepoint(mouse):
                self.selected_difficulty = "Easy"
                self.game.singleplayer_screen.difficulty = "Easy"

            elif self.normal_button.collidepoint(mouse):
                self.selected_difficulty = "Normal"
                self.game.singleplayer_screen.difficulty = "Normal"

            elif self.hard_button.collidepoint(mouse):
                self.selected_difficulty = "Hard"
                self.game.singleplayer_screen.difficulty = "Hard"

            # --- CONTINUE CLICK ---
            elif self.continue_button.collidepoint(mouse):

                # 1. Reset the deck and table!
                self.game.table.handle_start_game()

                # 2. Reset the specific game screen's scores and timers
                if hasattr(self.next_screen, 'reset_game_screen'):
                    self.next_screen.reset_game_screen()

                # 3. Transition to the game!
                self.game.current_screen = self.next_screen

    def draw(self, screen):
        """
        Description:
        Renders the control instructions, difficulty selection, and start interface.

        Function:
        Displays player controls at the top, shows difficulty selection for
        singleplayer mode, highlights selected options, and draws the Continue
        button to proceed to the game.
        """
        # Dark slate background
        screen.fill((44, 44, 62))
        mouse = pygame.mouse.get_pos()

        # --- TITLE & CONTROLS SECTION (TOP) ---
        title_text = self.game.title_font.render("Controls", True, WHITE)
        screen.blit(title_text, title_text.get_rect(center=(540, 80)))

        # 1. SPACE_BAR (Player 1)
        pygame.draw.rect(screen, WHITE, (150, 180, 240, 60), border_radius=8)
        pygame.draw.rect(screen, (150, 150, 150), (150, 180, 240, 60), width=4, border_radius=8)
        space_text = self.game.sub_font.render("SPACEBAR", True, DARK)
        screen.blit(space_text, space_text.get_rect(center=(270, 210)))

        p1_text = self.game.sub_font.render("Player 1 Call SET", True, WHITE)
        screen.blit(p1_text, p1_text.get_rect(center=(270, 270)))

        # 2. MOUSE (Selection)
        pygame.draw.rect(screen, WHITE, (490, 140, 100, 140), border_radius=40)
        pygame.draw.line(screen, DARK, (540, 140), (540, 200), 4)
        pygame.draw.line(screen, DARK, (490, 200), (590, 200), 4)

        mouse_text = self.game.sub_font.render("Left Click", True, WHITE)
        screen.blit(mouse_text, mouse_text.get_rect(center=(460, 310)))
        select_text = self.game.sub_font.render("Select Cards", True, WHITE)
        screen.blit(select_text, select_text.get_rect(center=(460, 340)))

        mouse_text2 = self.game.sub_font.render("Right Click", True, WHITE)
        screen.blit(mouse_text2, mouse_text2.get_rect(center=(620, 310)))
        unselect_text = self.game.sub_font.render("Unselect Cards", True, WHITE)
        screen.blit(unselect_text, unselect_text.get_rect(center=(620, 340)))

        if self.next_screen == self.game.game_screen:
            # 3. ENTER KEY (Player 2)
            pygame.draw.rect(screen, WHITE, (690, 180, 160, 60), border_radius=8)
            pygame.draw.rect(screen, (150, 150, 150), (690, 180, 160, 60), width=4, border_radius=8)
            enter_text = self.game.sub_font.render("ENTER", True, DARK)
            screen.blit(enter_text, enter_text.get_rect(center=(770, 210)))

            p2_text = self.game.sub_font.render("Player 2 Call SET", True, WHITE)
            screen.blit(p2_text, p2_text.get_rect(center=(770, 270)))

        if self.next_screen == self.game.singleplayer_screen:
            # --- DIFFICULTY SECTION (BOTTOM) ---
            diff_title = self.game.font.render("Choose Difficulty", True, WHITE)
            screen.blit(diff_title, diff_title.get_rect(center=(540, 430)))

        # Helper function to draw difficulty buttons
        def draw_diff_button(rect, text_str, is_selected):
            if self.next_screen == self.game.singleplayer_screen:
                # If selected, make it LIGHT. If hovered, make it slightly lighter DARK. Else DARK.
                if is_selected:
                    color = LIGHT
                elif rect.collidepoint(mouse):
                    color = (80, 80, 100)  # subtle hover color
                else:
                    color = DARK

                pygame.draw.rect(screen, color, rect, border_radius=12)

                # Draw a bright border if selected
                if is_selected:
                    pygame.draw.rect(screen, (0, 255, 255), rect, width=3, border_radius=12)
                else:
                    pygame.draw.rect(screen, WHITE, rect, width=2, border_radius=12)

                text_surf = self.game.sub_font.render(text_str, True, WHITE)
                screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Draw the 3 buttons
        draw_diff_button(self.easy_button, "Easy", self.selected_difficulty == "Easy")
        draw_diff_button(self.normal_button, "Normal", self.selected_difficulty == "Normal")
        draw_diff_button(self.hard_button, "Hard", self.selected_difficulty == "Hard")

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