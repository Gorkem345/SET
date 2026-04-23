import pygame
from utils.constants import WHITE, DARK, LIGHT
import random
from screens.PlayScreen import PlayScreen


class SingleplayerScreen(PlayScreen):
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        super().__init__(game)

        self.difficulty = "Normal"

        # Score system
        self.p1_score = 0  # initial score
        self.p2_score = 0
        self.comp_score = 0  # computer's score

        # Computer Timer setup
        self.comp_target_time = 0
        self.reset_computer_timer()

        self.comp_clicks_pending = []  # The list of cards it needs to click
        self.comp_next_click_time = 0  # When it is allowed to click the next card


    def reset_game_screen(self):
        """Resets all scores, timers, and the computer's brain for a fresh game."""
        super().reset_game_screen()
        self.p1_score = 0
        self.comp_score = 0

        # Completely Reset the Computer
        self.reset_computer_timer()  # Give it a fresh 8-20 seconds
        self.comp_clicks_pending = []  # Clear any queued clicks


    def clear_set_timer(self):
        super().clear_set_timer()
        self.reset_computer_timer()

    def resume_game_timer(self):
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += paused_duration
            self.comp_target_time += paused_duration
            self.paused = False


    def check_game_timeout(self):
        if self.get_game_time_left() <= 0:
            self.game.table.game_end = True
            if self.p1_score > self.comp_score:
                self.game.winner = "Player 1!"
            elif self.comp_score > self.p1_score:
                self.game.winner = "Computer!"
            else:
                self.game.winner = "Draw!"

            self.game.p1_score = self.p1_score
            self.game.comp_score = self.comp_score
            self.game.winner_screen.prev_screen = self.game.singleplayer_screen
            self.game.current_screen = self.game.winner_screen

            self.reset_game_screen()

    def check_winner(self):
        if not self.game.table.find_sets():
            self.game.table.game_end = True
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

            self.reset_game_screen()

    def reset_computer_timer(self):
        """Give the computer a random number of seconds to 'think'."""
        # Computer takes between 8 and 30 seconds depending on difficulty level
        if self.difficulty == "Easy":
            delay = random.randint(20000, 32000)
            self.comp_target_time = pygame.time.get_ticks() + delay
        if self.difficulty == "Normal":
            delay = random.randint(14000, 22000)
            self.comp_target_time = pygame.time.get_ticks() + delay
        if self.difficulty == "Hard":
            delay = random.randint(10000, 14000)
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
                        if self.correct_sound:
                            self.correct_sound.play()

                        self.show_message("SET !!!", 1500)
                        self.comp_score += self.game.point_gain
                        self.check_winner()
                    else:
                        if self.wrong_sound:
                            self.wrong_sound.play()

                        self.show_message("Not a set", 1500)
                        self.comp_score -= self.game.point_loss

                    self.clear_set_timer()
                    self.game.table.hinted = []

                else:
                    # We clicked card 1 or 2. Set the timer to wait 0.6 seconds before the next click!
                    self.comp_next_click_time = current_time + 1000

                    # We return here so the computer doesn't try to "think" while it's busy clicking
            return

        # --- STATE 2: The computer is "thinking" ---
        if self.active_player is None and current_time >= self.comp_target_time and not self.game.table.waiting_for_replace:

            set_indices = self.game.table.give_set()

            if set_indices:
                if self.set_sound and not self.game.table.selection_mode:
                    self.set_sound.play()
                # 1. Claim the turn! (2 represents the computer)
                self.start_set_timer(2)
                self.game.table.handle_start_selection()

                # 2. Put the 3 cards into the to-do list, computer can make a mistake
                a = 1
                if self.difficulty == "Easy":
                    a = 5
                elif self.difficulty == "Normal":
                    a = 8
                elif self.difficulty == "Hard":
                    a = 15
                randomInt = random.randint(1,a)

                if randomInt == 1:
                    # Computer makes a mistake
                    index_1 = (set_indices[0] + random.randint(1,11)) % 12
                    index_2 = (set_indices[1] + random.randint(1, 11)) % 12
                    index_3 = (set_indices[2] + random.randint(1, 11)) % 12
                    while index_1 == index_2 or index_2 == index_3 or index_1 == index_3:
                        index_2 = (set_indices[1] + random.randint(1,11)) % 12
                        index_3 = (set_indices[2] + random.randint(1,11)) % 12
                    self.comp_clicks_pending = [index_1, index_2, index_3]
                else:

                    self.comp_clicks_pending = [set_indices[0], set_indices[1], set_indices[2]]

                # 3. Wait 0.6 seconds before making the very first click
                self.comp_next_click_time = current_time + 800

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
                    if self.set_sound and not self.game.table.selection_mode:
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
                        self.pause_game_timer()
                        self.game.confirm_screen.open("restart_single")
                        self.game.current_screen = self.game.confirm_screen

                    # --- NEW: Menu Button ---
                    elif self.menu_button.collidepoint(mouse):
                        self.pause_game_timer()
                        self.game.confirm_screen.open("menu_single")
                        self.game.current_screen = self.game.confirm_screen

                    # 3. Check if they clicked a CARD
                    elif self.active_player is not None:
                        # Ask the board which card index the mouse is over
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None and self.active_player != 2:
                            if self.select_sound:
                                self.select_sound.play()
                            # Pass the click to your Table logic
                            forms_set = self.game.table.handle_click(clicked_index)

                            # If handle_click finished processing 3 cards, selection_mode will turn False
                            if not self.game.table.selection_mode:
                                if forms_set is not None:
                                    if forms_set:
                                        if self.correct_sound:
                                            self.correct_sound.play()

                                        self.show_message("SET", 1500)

                                        if self.active_player == 1:
                                            self.p1_score += self.game.point_gain
                                            self.check_winner()
                                        elif self.active_player == 2:
                                            self.comp_score += self.game.point_gain
                                            self.check_winner()
                                    else:
                                        if self.wrong_sound:
                                            self.wrong_sound.play()

                                        self.show_message("Not a set", 1500)

                                        if self.active_player == 1:
                                            self.p1_score -= self.game.point_loss
                                        elif self.active_player == 2:
                                            self.comp_score -= self.game.point_loss

                                self.clear_set_timer()
                                self.game.table.hinted = []

                elif event.button == 3:
                    if self.active_player is not None:
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None and self.active_player != 2:
                            self.game.table.handle_right_click(clicked_index)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        screen.blit(self.background, (0, 0))
        self.board.draw(screen)

        self.update_computer()

        # Timers
        time_left = self.get_time_left()
        game_time_left = self.get_game_time_left()
        self.check_game_timeout()

        # Left panel
        left_panel = pygame.Rect(20, 20, 280, 600)
        pygame.draw.rect(screen, (44, 44, 62), left_panel, border_radius=12)
        pygame.draw.rect(screen, WHITE, left_panel, 2, border_radius=12)

        # Score texts
        score_text = self.game.font.render("Score:", True, WHITE)
        p1_score_text = self.game.sub_font.render(
            f"Player 1:   {self.p1_score}", True, WHITE)
        comp_score_text = self.game.sub_font.render(
            f"Computer:   {self.comp_score}", True, WHITE)

        # Deck info
        cards_left = len(self.game.table.deck)
        deck_count_text = self.game.sub_font.render(
            f"Cards in deck: {cards_left}", True, WHITE)

        # Game time
        minutes = game_time_left // 60
        seconds = game_time_left % 60
        game_duration_text = self.game.sub_font.render(
            f"Game time: {minutes}:{seconds:02}", True, WHITE
        )

        screen.blit(score_text, (left_panel.x + 20, left_panel.y + 30))
        screen.blit(p1_score_text, (left_panel.x + 20, left_panel.y + 85))
        screen.blit(comp_score_text, (left_panel.x + 20, left_panel.y + 125))
        screen.blit(game_duration_text, (left_panel.x + 20, left_panel.y + 185))
        screen.blit(deck_count_text, (left_panel.x + 20, left_panel.y + 235))

        # Button positions
        self.setbutton.center = (left_panel.centerx, left_panel.y + 345)
        self.hint_button.center = (left_panel.centerx, left_panel.y + 420)
        self.restart_button.center = (left_panel.x + 75, left_panel.y + 550)
        self.menu_button.center = (left_panel.x + 195, left_panel.y + 550)

        # Button texts
        sethint_text1 = self.game.sub_font.render("P1 press Space", True, WHITE)
        hint_text = self.game.sub_font.render("HINT", True, WHITE)
        restart_text = self.game.small_font.render("RESTART", True, WHITE)
        menu_text = self.game.small_font.render("MENU", True, WHITE)

        # SET info box
        pygame.draw.rect(screen, DARK, self.setbutton, border_radius=12)
        screen.blit(
            sethint_text1,
            sethint_text1.get_rect(
                center=(self.setbutton.centerx, self.setbutton.centery))
        )

        # HINT button
        pygame.draw.rect(
            screen,
            LIGHT if self.hint_button.collidepoint(mouse) else DARK,
            self.hint_button,
            border_radius=12
        )
        screen.blit(hint_text,
                    hint_text.get_rect(center=self.hint_button.center))

        # RESTART button
        pygame.draw.rect(
            screen,
            LIGHT if self.restart_button.collidepoint(mouse) else DARK,
            self.restart_button,
            border_radius=12
        )
        screen.blit(restart_text,
                    restart_text.get_rect(center=self.restart_button.center))

        # MENU button
        pygame.draw.rect(
            screen,
            LIGHT if self.menu_button.collidepoint(mouse) else DARK,
            self.menu_button,
            border_radius=12
        )
        screen.blit(menu_text,
                    menu_text.get_rect(center=self.menu_button.center))

        # Message panel
        message_panel = pygame.Rect(20, 630, 280, 80)
        pygame.draw.rect(screen, (44, 44, 62), message_panel, border_radius=12)
        pygame.draw.rect(screen, WHITE, message_panel, 2, border_radius=12)

        current_time = pygame.time.get_ticks()

        if current_time < self.message_end_time:
            message_text = self.game.sub_font.render(self.status_message, True,
                                                     WHITE)
        else:
            if self.active_player == 1:
                message_text = self.game.sub_font.render(
                    "Player 1 is answering", True, WHITE)
            elif self.active_player == 2:
                message_text = self.game.sub_font.render(
                    "Computer is answering", True, WHITE)
            else:
                message_text = self.game.sub_font.render("Press set when ready",
                                                         True, WHITE)

        timer_text = self.game.sub_font.render(f"Time left: {time_left}s", True,
                                               WHITE)

        screen.blit(message_text, (message_panel.x + 20, message_panel.y + 10))
        screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 40))