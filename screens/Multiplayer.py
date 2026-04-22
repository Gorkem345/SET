import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
from screens.PlayScreen import PlayScreen


class Multiplayer(PlayScreen):
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        super().__init__(game)

        # Score
        self.p1_score = 0
        self.p2_score = 0
        self.comp_score = 0

    def reset_game_screen(self):
        super().reset_game_screen()
        self.p1_score = 0
        self.p2_score = 0


    def check_game_timeout(self):
        if self.get_game_time_left() <= 0:
            self.game.table.game_end = True
            if self.p1_score > self.p2_score:
                self.game.winner = "Player 1!"
            elif self.p2_score > self.p1_score:
                self.game.winner = "Player 2!"
            else:
                self.game.winner = "Draw!"

            self.game.p1_score = self.p1_score
            self.game.p2_score = self.p2_score
            self.game.winner_screen.prev_screen = self.game.game_screen
            self.game.current_screen = self.game.winner_screen

            self.reset_game_screen()

    #pause and resume function
    def pause(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()

    def resume(self):
        if self.paused:
            pause_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += pause_duration
            self.paused = False


    def check_winner(self):
        # GameScreen knows Game
        # WinnerScreen knows Game
        # WinnerScreen does not know Gamescreen
        # in this case you need self.game (Game object), store the score and winner
        # as an attribute of Game object so that it can access to WinnerScreen

        if not self.game.table.find_sets():
            self.game.table.game_end = True
            if self.p1_score > self.p2_score:
                self.game.winner = "Player 1!"


            elif self.p1_score < self.p2_score:
                self.game.winner = "Player 2!"

            else:
                self.game.winner = "Player 1 and Player 2!"

            self.game.p1_score = self.p1_score
            self.game.p2_score = self.p2_score
            self.game.winner_screen.prev_screen = self.game.game_screen
            self.game.current_screen = self.game.winner_screen

            # reset timer, score and the game
            self.clear_set_timer()
            self.p1_score = 0  # initial score
            self.p2_score = 0
            self.game.table.handle_start_game()



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

                # Player 2 hits ENTER (Return)
                elif event.key == pygame.K_RETURN:
                    if self.set_sound and not self.game.table.selection_mode:
                        self.set_sound.play()
                    if self.active_player is None:
                        self.start_set_timer(2)
                        self.game.table.handle_start_selection()


            # --- MOUSE EVENTS (For UI and Cards) ---

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    # 2. Check if they clicked the HINT button
                    if self.hint_button.collidepoint(mouse):
                        hint_indices = self.game.table.give_hint()
                        if hint_indices:
                            self.game.table.hinted = hint_indices

                    # Restart
                    elif self.restart_button.collidepoint(mouse):
                        self.pause_game_timer()
                        self.game.confirm_screen.open("restart")
                        self.game.current_screen = self.game.confirm_screen

                    # Back to menu
                    elif self.menu_button.collidepoint(mouse):
                        self.pause_game_timer()
                        self.game.confirm_screen.open("menu")
                        self.game.current_screen = self.game.confirm_screen


                    # 3. Check if they clicked a CARD
                    elif self.active_player is not None:
                        # Ask the board which card index the mouse is over
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None:
                            if self.select_sound:
                                self.select_sound.play()
                            # Pass the click to your Table logic
                            forms_set = self.game.table.handle_click(clicked_index)

                            # If handle_click finished processing 3 cards, selection_mode will turn False
                            if not self.game.table.selection_mode:

                                if forms_set is not None:
                                    if forms_set:
                                        # Play Correct Sound
                                        if self.correct_sound:
                                            self.correct_sound.play()

                                        self.show_message("SET !!!", 1500)

                                        if self.active_player == 1:
                                            self.p1_score += self.game.point_gain
                                            self.check_winner()
                                        elif self.active_player == 2:
                                            self.p2_score += self.game.point_gain
                                            self.check_winner()
                                    else:
                                        # Play Wrong Sound
                                        if self.wrong_sound:
                                            self.wrong_sound.play()

                                        self.show_message("Not a set", 1500)

                                        if self.active_player == 1:
                                            self.p1_score -= self.game.point_loss
                                        elif self.active_player == 2:
                                            self.p2_score -= self.game.point_loss

                                # Stop the timer and end the turn
                                self.clear_set_timer()
                                # Clear hints
                                self.game.table.hinted = []

                elif event.button == 3:
                    if self.active_player is not None:
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None:
                            self.game.table.handle_right_click(clicked_index)

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        screen.blit(self.background, (0, 0))
        self.board.draw(screen)

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
        p1_score_text = self.game.sub_font.render(f"Player 1:   {self.p1_score}", True, WHITE)
        p2_score_text = self.game.sub_font.render(f"Player 2:   {self.p2_score}", True, WHITE)


        # Deck info
        cards_left = len(self.game.table.deck)

        deck_count_text = self.game.sub_font.render(f"Cards in deck: {cards_left}", True, WHITE)

        minutes = game_time_left // 60
        seconds = game_time_left % 60
        game_duration_text = self.game.sub_font.render(
            f"Game time: {minutes}:{seconds:02}", True, WHITE
        )

        screen.blit(score_text, (left_panel.x + 20, left_panel.y + 30))
        screen.blit(p1_score_text, (left_panel.x + 20, left_panel.y + 85))
        screen.blit(p2_score_text, (left_panel.x + 20, left_panel.y + 125))
        screen.blit(game_duration_text, (left_panel.x + 20, left_panel.y + 185))


        screen.blit(deck_count_text, (left_panel.x + 20, left_panel.y + 235))

        # Button positions
        self.setbutton.center = (left_panel.centerx, left_panel.y + 345)
        self.hint_button.center = (left_panel.centerx, left_panel.y + 420)
        self.restart_button.center = (left_panel.x + 75, left_panel.y + 550)
        self.menu_button.center = (left_panel.x + 195, left_panel.y + 550)

        # Button texts
        sethint_text1 = self.game.sub_font.render("P1 press Space", True, WHITE)
        sethint_text2 = self.game.sub_font.render("P2 press Enter", True, WHITE)
        hint_text = self.game.sub_font.render("HINT", True, WHITE)
        restart_text = self.game.small_font.render("RESTART", True, WHITE)
        menu_text = self.game.small_font.render("MENU", True, WHITE)

        # SET info box
        pygame.draw.rect(screen, DARK, self.setbutton, border_radius=12)
        screen.blit(
            sethint_text1,
            sethint_text1.get_rect(center=(self.setbutton.centerx, self.setbutton.centery - 15))
        )
        screen.blit(
            sethint_text2,
            sethint_text2.get_rect(center=(self.setbutton.centerx, self.setbutton.centery + 15))
        )

        # HINT button
        pygame.draw.rect(
            screen,
            LIGHT if self.hint_button.collidepoint(mouse) else DARK,
            self.hint_button,
            border_radius=12
        )
        screen.blit(hint_text, hint_text.get_rect(center=self.hint_button.center))

        # RESTART button
        pygame.draw.rect(
            screen,
            LIGHT if self.restart_button.collidepoint(mouse) else DARK,
            self.restart_button,
            border_radius=12
        )
        screen.blit(restart_text, restart_text.get_rect(center=self.restart_button.center))

        # MENU button
        pygame.draw.rect(
            screen,
            LIGHT if self.menu_button.collidepoint(mouse) else DARK,
            self.menu_button,
            border_radius=12
        )
        screen.blit(menu_text, menu_text.get_rect(center=self.menu_button.center))

        # Message panel
        message_panel = pygame.Rect(20, 630, 280, 80)
        pygame.draw.rect(screen, (44, 44, 62), message_panel, border_radius=12)
        pygame.draw.rect(screen, WHITE, message_panel, 2, border_radius=12)

        current_time = pygame.time.get_ticks()

        if current_time < self.message_end_time:
            message_text = self.game.sub_font.render(self.status_message, True,
                                                     WHITE)
        else:
            if self.active_player is not None:
                message_text = self.game.sub_font.render(
                    f"Player {self.active_player} is answering", True, WHITE
                )
            else:
                message_text = self.game.sub_font.render("Press set when ready",
                                                         True, WHITE)

        timer_text = self.game.sub_font.render(f"Time left: {time_left}s", True,
                                               WHITE)

        screen.blit(message_text, (message_panel.x + 20, message_panel.y + 10))
        screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 40))