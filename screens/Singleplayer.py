import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
import random
import time


class SingleplayerScreen:
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        self.game = game  # game here is the Game object, so self.game = Game()
        self.board = Display_board(game)
        # Player interface
        self.setbutton = pygame.Rect(200, 80, 198, 80)

        self.difficulty = "Normal"

        # testing button
        #self.plus = pygame.Rect(500, 80, 100, 40)

        # HINT button
        self.hint_button = pygame.Rect(0, 0, 100, 40)

        # --- NEW BUTTONS ---
        self.restart_button = pygame.Rect(0, 0, 100, 50)
        self.menu_button = pygame.Rect(0, 0, 100, 50)

        # -----------------------------
        # Score system
        # -----------------------------
        self.p1_score = 0  # initial score
        self.comp_score = 0  # computer's score

        # Which player pressed SET?
        self.active_player = None

        # Timer settings
        self.set_time_limit = 15000  # 15000 milliseconds = 15 seconds
        self.set_start_time = 0

        # Winner
        self.winner = None

        # Computer Timer setup
        self.comp_target_time = 0
        self.reset_computer_timer()

        self.comp_clicks_pending = []  # The list of cards it needs to click
        self.comp_next_click_time = 0  # When it is allowed to click the next card

        # load table background
        # I only want the center part of the image
        img = pygame.image.load("images/table.png").convert()
        img_w, img_h = img.get_size()
        screen_w, screen_h = 1080, 720
        x = (img_w - screen_w) // 2
        y = (img_h - screen_h) // 2

        self.background = img.subsurface((x, y, screen_w, screen_h))

        try:
            self.correct_sound = pygame.mixer.Sound("sounds/correct.wav")
            self.wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")
            self.set_sound = pygame.mixer.Sound("sounds/set.wav")

            # Optional: adjust volume (0.0 to 1.0)
            self.correct_sound.set_volume(0.4)
            self.wrong_sound.set_volume(0.5)
            self.set_sound.set_volume(0.5)

        except Exception as e:
            print(f"Could not load sounds: {e}")
            self.correct_sound = None
            self.wrong_sound = None
            self.set_sound = None

    def reset_game_screen(self):
        """Resets all scores, timers, and the computer's brain for a fresh game."""
        self.p1_score = 0
        self.comp_score = 0
        self.winner = None
        self.clear_set_timer()

        # Reset the 5-minute game timer (if you are using it here)
        self.game_start_time = pygame.time.get_ticks()

        # Reset the table
        self.game.table.selection_mode = False
        self.game.table.selected = []
        self.game.table.hinted = []
        self.game.table.handle_start_game()

        # Completely Reset the Computer
        self.reset_computer_timer()  # Give it a fresh 8-20 seconds
        self.comp_clicks_pending = []  # Clear any queued clicks
        self.computer_showing_set = False  # Stop it from showing old hints

    def start_set_timer(self, player):
        """Start the 15-second answer period for one player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()  # it is the time pass when the game start until you click SET button
        # a = f'set_start_time: {self.set_start_time}' #Debug
        # print(a)

    def clear_set_timer(self):
        """Stop the answer period."""
        self.active_player = None
        self.set_start_time = 0

        self.reset_computer_timer()

    def get_time_left(self):
        """Return remaining time in seconds. If no timer, return 15''."""

        if self.active_player is None:
            return "%d" % 15

        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.set_start_time
        remaining = self.set_time_limit - elapsed

        if remaining <= 0:
            # Clear the highlighted cards when time is up!
            self.game.table.selection_mode = False
            self.game.table.selected = []
            self.game.table.hinted = []

            if self.active_player == 1:
                self.p1_score -= 1
            elif self.active_player == 2:
                self.comp_score -= 1

            self.clear_set_timer()
            return 0

        return remaining // 1000 + 1

    def check_winner(self):

        if not self.game.table.find_sets():
            if self.p1_score > self.comp_score:
                self.game.winner = "Player 1!"


            elif self.p1_score < self.comp_score:
                self.game.winner = "Computer!"

            else:
                self.game.winner = "Player 1 and Computer!"

            self.game.p1_score = self.p1_score
            self.game.comp_score = self.comp_score
            self.game.winner_screen.prev_screen = self.game.singleplayer_screen
            self.game.current_screen = self.game.winner_screen

            # reset timer, score and the game
            self.clear_set_timer()
            self.p1_score = 0  # initial score
            self.comp_score = 0
            self.game.table.handle_start_game()

    def reset_computer_timer(self):
        """Give the computer a random number of seconds to 'think'."""
        # Computer takes between 8 and 30 seconds depending on difficulty level
        if self.difficulty == "Easy":
            delay = random.randint(18000, 30000)
            self.comp_target_time = pygame.time.get_ticks() + delay
        if self.difficulty == "Normal":
            delay = random.randint(12000, 20000)
            self.comp_target_time = pygame.time.get_ticks() + delay
        if self.difficulty == "Hard":
            delay = random.randint(8000, 12000)
            self.comp_target_time = pygame.time.get_ticks() + delay

    def update_computer(self):
        current_time = pygame.time.get_ticks()

        # --- STATE 1: The computer is currently in the middle of clicking its 3 cards ---
        if len(self.comp_clicks_pending) > 0:

            # Is it time to click the next card?
            if current_time >= self.comp_next_click_time:

                # Take the first card out of the queue and click it!
                next_card = self.comp_clicks_pending.pop(0)
                forms_set = self.game.table.handle_click(next_card)

                # Did we just click the 3rd and final card?
                if not self.game.table.selection_mode:
                    if forms_set:
                        if hasattr(self, 'correct_sound') and self.correct_sound:
                            self.correct_sound.play()
                        self.comp_score += 1
                        self.check_winner()

                    # Turn is over, reset everything
                    self.clear_set_timer()
                    self.game.table.hinted = []

                else:
                    # We clicked card 1 or 2. Set the timer to wait 0.6 seconds before the next click!
                    self.comp_next_click_time = current_time + 1000

                    # We return here so the computer doesn't try to "think" while it's busy clicking
            return

        # --- STATE 2: The computer is "thinking" ---
        if self.active_player is None and current_time >= self.comp_target_time and not self.game.table.waiting_for_replace:

            hint_indices = self.game.table.give_set()

            if hint_indices:
                if self.set_sound:
                    self.set_sound.play()
                # 1. Claim the turn! (2 represents the computer)
                self.start_set_timer(2)
                self.game.table.handle_start_selection()

                # 2. Put the 3 cards into the to-do list
                self.comp_clicks_pending = [hint_indices[0], hint_indices[1], hint_indices[2]]

                # 3. Wait 0.6 seconds before making the very first click
                self.comp_next_click_time = current_time + 600

            else:
                # No sets on the board, check again in 1 second
                self.comp_target_time = current_time + 1000

    def handle_event(self, event):
        if not self.game.table.waiting_for_replace:
            mouse = pygame.mouse.get_pos()  # get mouse position

            # --- KEYBOARD EVENTS (For SET calls) ---
            if event.type == pygame.KEYDOWN:
                # Player 1 hits SPACEBAR
                if event.key == pygame.K_SPACE:
                    if self.set_sound:
                        self.set_sound.play()
                    if self.active_player is None:
                        self.start_set_timer(1)
                        self.game.table.handle_start_selection()


            # --- MOUSE EVENTS (For UI and Cards) ---

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    # 2. Check if they clicked the HINT button
                    if self.hint_button.collidepoint(mouse):
                        hint_indices = self.game.table.give_hint()
                        if hint_indices:
                            self.game.table.hinted = hint_indices

                    # --- NEW: Restart Button ---
                    elif self.restart_button.collidepoint(mouse):
                        self.reset_game_screen()

                    # --- NEW: Menu Button ---
                    elif self.menu_button.collidepoint(mouse):
                        self.game.current_screen = self.game.start_screen
                        self.reset_game_screen()

                    # 3. Check if they clicked a CARD
                    elif self.active_player is not None:
                        # Ask the board which card index the mouse is over
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None and self.active_player != 2:
                            # Pass the click to your Table logic
                            forms_set = self.game.table.handle_click(clicked_index)

                            # If handle_click finished processing 3 cards, selection_mode will turn False
                            if not self.game.table.selection_mode:
                                # (Ideally, you check if they actually got it right here to award points)
                                if forms_set is not None:
                                    if forms_set:
                                        if self.correct_sound:
                                            self.correct_sound.play()
                                        if self.active_player == 1:
                                            self.p1_score += 1
                                            self.check_winner()
                                        elif self.active_player == 2:
                                            self.comp_score += 1
                                            self.check_winner()
                                    else:
                                        if self.wrong_sound:
                                            self.wrong_sound.play()
                                        if self.active_player == 1:
                                            self.p1_score -= 1
                                        elif self.active_player == 2:
                                            self.comp_score -= 1
                                # Stop the timer and end the turn
                                self.clear_set_timer()
                                # Clear hints
                                self.game.table.hinted = []

                elif event.button == 3:
                    if self.active_player is not None:
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None and self.active_player != 2:
                            self.game.table.handle_right_click(clicked_index)


    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        self.check_winner()

        self.update_computer()

        # show background
        screen.blit(self.background, (0, 0))

        # Display the board
        self.board.draw(screen)

        # Check timer every frame
        time_left = self.get_time_left()

        # LEFT PANEL (Increased height to 600)
        left_panel = pygame.Rect(20, 20, 280, 600)  # topleft x, y, width, height

        # panel background
        pygame.draw.rect(screen, (44, 44, 62), left_panel, border_radius=12)

        # panel border
        pygame.draw.rect(screen, WHITE, left_panel, 2, border_radius=12)

        # TEXTS
        score_text = self.game.font.render("Score:", True, WHITE)
        p1_score_text = self.game.sub_font.render(f"Player 1:   {self.p1_score}",
                                                  True, WHITE)

        comp_score_text = self.game.sub_font.render(f"Computer:   {self.comp_score}",
                                                  True, WHITE)

        # change from absolute position to relative position of the panel
        screen.blit(score_text, (left_panel.x + 20, left_panel.y + 45))
        screen.blit(p1_score_text, (left_panel.x + 20, left_panel.y + 105))
        screen.blit(comp_score_text, (left_panel.x + 20, left_panel.y + 145))

        # BUTTON POSITIONS INSIDE PANEL
        self.setbutton.center = (left_panel.centerx, left_panel.y + 250)
        self.hint_button.center = (left_panel.centerx, left_panel.y + 350)
        # --- NEW BUTTON POSITIONS ---
        self.restart_button.center = (left_panel.x + 75, left_panel.y + 550)
        self.menu_button.center = (left_panel.x + 195, left_panel.y + 550)

        # BUTTON TEXTS
        sethint_text1 = self.game.sub_font.render('P1 press Space', True, WHITE)
        hint_text = self.game.sub_font.render("HINT", True, WHITE)
        # --- NEW BUTTON TEXTS ---
        restart_text = self.game.small_font.render("RESTART", True, WHITE)
        menu_text = self.game.small_font.render("MENU", True, WHITE)

        # DRAW BUTTONS
        # -------------------------

        # Disabled the hover effect for the SET box so it acts just as a label
        pygame.draw.rect(
            screen,
            DARK,
            self.setbutton,
            border_radius=12
        )
        screen.blit(sethint_text1,
                    sethint_text1.get_rect(center=(self.setbutton.centerx, self.setbutton.centery)))

        # Draw HINT button
        pygame.draw.rect(
            screen,
            LIGHT if self.hint_button.collidepoint(mouse) else DARK,
            self.hint_button,
            border_radius=12
        )
        screen.blit(hint_text, hint_text.get_rect(center=self.hint_button.center))

        # --- Draw RESTART button ---
        pygame.draw.rect(
            screen,
            LIGHT if self.restart_button.collidepoint(mouse) else DARK,
            self.restart_button,
            border_radius=12
        )
        screen.blit(restart_text, restart_text.get_rect(center=self.restart_button.center))

        # --- Draw MENU button ---
        pygame.draw.rect(
            screen,
            LIGHT if self.menu_button.collidepoint(mouse) else DARK,
            self.menu_button,
            border_radius=12
        )
        screen.blit(menu_text, menu_text.get_rect(center=self.menu_button.center))

        # Timer / message panel (Adjusted Y to 630 and height to 80 to fit under the new taller panel)
        message_panel = pygame.Rect(20, 630, 280, 80)
        pygame.draw.rect(screen, (44, 44, 62), message_panel, border_radius=12)
        pygame.draw.rect(screen, WHITE, message_panel, 2, border_radius=12)

        if self.active_player is not None:
            turn_text = self.game.sub_font.render(
                f"Player {self.active_player} is answering", True, WHITE
            )
            timer_text = self.game.sub_font.render(
                f"Time left: {time_left}s", True, WHITE
            )
            screen.blit(turn_text, (message_panel.x + 20, message_panel.y + 10))
            screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 40))
        else:
            wait_text = self.game.sub_font.render("Press set when ready", True, WHITE)
            screen.blit(wait_text, (message_panel.x + 20, message_panel.y + 10))

            timer_text = self.game.sub_font.render(f"Time left: {time_left}s", True, WHITE)
            screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 40))