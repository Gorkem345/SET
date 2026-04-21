import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table


class GameScreen:
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        self.game = game  # game here is the Game object, so self.game = Game()
        self.board = Display_board(game)

        # UI buttons
        self.setbutton = pygame.Rect(200, 80, 198, 80)
        self.hint_button = pygame.Rect(0, 0, 100, 40)
        self.restart_button = pygame.Rect(0, 0, 100, 50)
        self.menu_button = pygame.Rect(0, 0, 100, 50)

        # Score
        self.p1_score = 0
        self.p2_score = 0

        # Active answering player
        self.active_player = None

        # 15-second SET timer
        self.set_time_limit = 15000
        self.set_start_time = 0

        # Whole game timer: 5 minutes
        self.game_duration = 301000
        self.game_start_time = pygame.time.get_ticks()
        #remember when the GameScreen is created not the time when you hit multiplayer play

        #winner
        self.winner = None

        #Game pause timer
        self.paused = False
        self.pause_start_time = 0

        #messager panel
        self.status_message = "Press set when ready"
        self.message_end_time = 0

        # Background
        img = pygame.image.load("images/table.png").convert()
        img_w, img_h = img.get_size()
        screen_w, screen_h = 1080, 720
        x = (img_w - screen_w) // 2
        y = (img_h - screen_h) // 2
        self.background = img.subsurface((x, y, screen_w, screen_h))

        try:
            self.correct_sound = pygame.mixer.Sound("sounds/correct.wav")
            self.wrong_sound = pygame.mixer.Sound("sounds/wrong.wav")

            # Optional: adjust volume (0.0 to 1.0)
            self.correct_sound.set_volume(0.5)
            self.wrong_sound.set_volume(0.5)
        except Exception as e:
            print(f"Could not load sounds: {e}")
            self.correct_sound = None
            self.wrong_sound = None

    def start_set_timer(self, player):
        """Start the 15-second answer period for one player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()  # it is the time pass when the game start until you click SET button


    def clear_set_timer(self):
        """Stop the answer period."""
        self.active_player = None
        self.set_start_time = 0

    def get_time_left(self):
        """Return remaining time in seconds. If no timer, return 15''."""

        if self.active_player is None:
            return 15

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
                self.p2_score -= 1

            self.show_message("Time's up!", 1500)
            self.clear_set_timer()
            return 0

        return remaining // 1000 + 1

    def get_game_time_left(self):
        #current_time = pygame.time.get_ticks() #the time now (since the program start)
        #elapsed = current_time - self.game_start_time #time is the moment when  GameScreen created
        #remaining = self.game_duration - elapsed #since the program keep running, the elapse keep moving forward
                                                 #at first it is the time gap between NOW - Gamescreen create
                                                 #then it is time now + 1 - gamescreen created
                                                 # so on.

        if self.paused:
            current_time = self.pause_start_time
        else:
            current_time = pygame.time.get_ticks()

        elapsed = current_time - self.game_start_time
        remaining = self.game_duration - elapsed

        if remaining <= 0:
            return 0

        return remaining // 1000

    def reset_game_screen(self):
        self.p1_score = 0
        self.p2_score = 0
        self.winner = None
        self.clear_set_timer()

        self.game_start_time = pygame.time.get_ticks()

        # Reset table state too
        self.game.table.selection_mode = False
        self.game.table.selected = []
        self.game.table.hinted = []
        self.game.table.handle_start_game()

    def check_game_timeout(self):
        if self.get_game_time_left() <= 0:
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

    def pause_game_timer(self):
        if not self.paused:
            self.paused = True
            self.pause_start_time = pygame.time.get_ticks()

    def resume_game_timer(self):
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += paused_duration
            self.paused = False

    def check_winner(self):
        # GameScreen knows Game
        # WinnerScreen knows Game
        # WinnerScreen does not know Gamescreen
        # in this case you need self.game (Game object), store the score and winner
        # as an attribute of Game object so that it can access to WinnerScreen

        if not self.game.table.find_sets():
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

    #show different message based on user action result
    def show_message(self, text, duration=1500):
        self.status_message = text
        self.message_end_time = pygame.time.get_ticks() + duration

    def handle_event(self, event):
        if not self.game.table.waiting_for_replace:
            mouse = pygame.mouse.get_pos()  # get mouse position

            # --- KEYBOARD EVENTS (For SET calls) ---
            if event.type == pygame.KEYDOWN:
                # Player 1 hits SPACEBAR
                if event.key == pygame.K_SPACE:
                    if self.active_player is None:
                        self.start_set_timer(1)
                        self.game.table.handle_start_selection()

                # Player 2 hits ENTER (Return)
                elif event.key == pygame.K_RETURN:
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
                        self.reset_game_screen()

                    # Back to menu
                    elif self.menu_button.collidepoint(mouse):

                        self.game.current_screen = self.game.start_screen
                        self.reset_game_screen()


                    # 3. Check if they clicked a CARD
                    elif self.active_player is not None:
                        # Ask the board which card index the mouse is over
                        clicked_index = self.board.get_clicked_card_index(mouse)

                        if clicked_index is not None:
                            # Pass the click to your Table logic
                            forms_set = self.game.table.handle_click(clicked_index)

                            # If handle_click finished processing 3 cards, selection_mode will turn False
                            if not self.game.table.selection_mode:

                                if forms_set is not None:
                                    if forms_set:
                                        # Play Correct Sound
                                        if self.correct_sound:
                                            self.correct_sound.play()

                                        if self.active_player == 1:
                                            self.p1_score += 1
                                            self.check_winner()
                                        elif self.active_player == 2:
                                            self.p2_score += 1
                                            self.check_winner()
                                    else:
                                        # Play Wrong Sound
                                        if self.wrong_sound:
                                            self.wrong_sound.play()

                                        if self.active_player == 1:
                                            self.p1_score -= 1
                                        elif self.active_player == 2:
                                            self.p2_score -= 1

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

        screen.blit(score_text, (left_panel.x + 20, left_panel.y + 45))
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