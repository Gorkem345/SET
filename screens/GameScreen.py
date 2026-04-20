import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table


class GameScreen:
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        self.game = game  # game here is the Game object, so self.game = Game()
        self.board = Display_board(game)
        # Player interface
        self.setbutton = pygame.Rect(200, 80, 198, 80)

        # testing button
        #self.plus = pygame.Rect(500, 80, 100, 40)

        # HINT button
        self.hint_button = pygame.Rect(0, 0, 100, 40)

        # -----------------------------
        # Score system
        # -----------------------------
        self.p1_score = 0  # initial score
        self.p2_score = 0

        # Which player pressed SET?
        self.active_player = None

        # Timer settings
        self.set_time_limit = 15000  # 15000 milliseconds = 15 seconds
        self.set_start_time = 0

        # Winner: Score > 30
        self.winner = None

        # load table background
        # I only want the center part of the image
        img = pygame.image.load("images/table.png").convert()
        img_w, img_h = img.get_size()
        screen_w, screen_h = 1080, 720
        x = (img_w - screen_w) // 2
        y = (img_h - screen_h) // 2

        self.background = img.subsurface((x, y, screen_w, screen_h))

    def start_set_timer(self, player):
        """Start the 15-second answer period for one player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks()  # it is the time pass when the game start until you click SET button
        # a = f'set_start_time: {self.set_start_time}'
        # print(a)

    def clear_set_timer(self):
        """Stop the answer period."""
        self.active_player = None
        self.set_start_time = 0

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
                self.p2_score -= 1

            self.clear_set_timer()
            return 0

        return remaining // 1000 + 1

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
            self.game.current_screen = self.game.winner_screen

            # reset timer, score and the game
            self.clear_set_timer()
            self.p1_score = 0  # initial score
            self.p2_score = 0
            self.game.table.handle_start_game()

    def handle_event(self, event):
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

            '''
            # 1. Check if they clicked the PLUS button
            if self.plus.collidepoint(mouse):
                if self.active_player == 1:
                    self.p1_score += 1
                    self.check_winner()
                elif self.active_player == 2:
                    self.p2_score += 1
                    self.check_winner()
            '''

            # 2. Check if they clicked the HINT button
            if self.hint_button.collidepoint(mouse):
                hint_indices = self.game.table.give_hint()
                if hint_indices:
                    self.game.table.hinted = hint_indices

            # 3. Check if they clicked a CARD
            elif self.active_player is not None:
                # Ask the board which card index the mouse is over
                clicked_index = self.board.get_clicked_card_index(mouse)

                if clicked_index is not None:
                    # Pass the click to your Table logic
                    forms_set = self.game.table.handle_click(clicked_index)

                    # If handle_click finished processing 3 cards, selection_mode will turn False
                    if not self.game.table.selection_mode:
                        # (Ideally, you check if they actually got it right here to award points)
                        if forms_set is not None:
                            if forms_set:
                                if self.active_player == 1:
                                    self.p1_score += 1
                                    self.check_winner()
                                elif self.active_player == 2:
                                    self.p2_score += 1
                                    self.check_winner()
                            else:
                                if self.active_player == 1:
                                    self.p1_score -= 1
                                elif self.active_player == 2:
                                    self.p2_score -= 1
                        # Stop the timer and end the turn
                        self.clear_set_timer()
                        # Clear hints
                        self.game.table.hinted = []

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()

        # show background
        screen.blit(self.background, (0, 0))

        # Display the board
        self.board.draw(screen)

        # Check timer every frame
        time_left = self.get_time_left()

        # LEFT PANEL
        left_panel = pygame.Rect(20, 20, 280, 500)  # topleft x, y, width, height

        # panel background
        pygame.draw.rect(screen, (44, 44, 62), left_panel, border_radius=12)
        # where to draw: screen, what color, recantagle: left_panel,
        # border_radius, Instead of sharp 90° corners, the rectangle gets rounded corners

        # panel border
        pygame.draw.rect(screen, WHITE, left_panel, 2, border_radius=12)

        # TEXTS
        score_text = self.game.font.render("Score:", True, WHITE)
        p1_score_text = self.game.sub_font.render(f"Player 1:   {self.p1_score}",
                                                  True, WHITE)

        p2_score_text = self.game.sub_font.render(f"Player 2:   {self.p2_score}",
                                                  True, WHITE)

        # change from absolute position to relative position of the panel

        screen.blit(score_text, (left_panel.x + 20, left_panel.y + 45))
        screen.blit(p1_score_text, (left_panel.x + 20, left_panel.y + 105))
        screen.blit(p2_score_text, (left_panel.x + 20, left_panel.y + 145))

        # BUTTON POSITIONS INSIDE PANEL
        self.setbutton.center = (left_panel.centerx, left_panel.y + 250)
        #self.plus.center = (left_panel.centerx, left_panel.y + 300)
        self.hint_button.center = (left_panel.centerx, left_panel.y + 350)

        # BUTTON TEXTS
        #set_text = self.game.sub_font.render("SET", True, WHITE)
        sethint_text1 = self.game.sub_font.render('P1 press Space', True, WHITE)
        sethint_text2 = self.game.sub_font.render('P2 press Enter', True, WHITE)
        #plus_text = self.game.sub_font.render("PLUS", True, WHITE)
        hint_text = self.game.sub_font.render("HINT", True, WHITE)

        # DRAW BUTTONS
        # -------------------------

        # Disabled the hover effect for the SET box so it acts just as a label
        pygame.draw.rect(
            screen,
            DARK,
            self.setbutton,
            border_radius=12
        )
        #screen.blit(set_text,
        #           set_text.get_rect(center=(self.setbutton.centerx, self.setbutton.centery - 15)))
        screen.blit(sethint_text1,
                    sethint_text1.get_rect(center=(self.setbutton.centerx, self.setbutton.centery - 15)))
        screen.blit(sethint_text2,
                    sethint_text2.get_rect(center=(self.setbutton.centerx, self.setbutton.centery + 15)))

        '''
        pygame.draw.rect(
            screen,
            LIGHT if self.plus.collidepoint(mouse) else DARK,
            self.plus,
            border_radius=12
        )
        '''
        #screen.blit(plus_text, plus_text.get_rect(center=self.plus.center))

        # Draw HINT button
        pygame.draw.rect(
            screen,
            LIGHT if self.hint_button.collidepoint(mouse) else DARK,
            self.hint_button,
            border_radius=12
        )
        screen.blit(hint_text, hint_text.get_rect(center=self.hint_button.center))

        # Timer / message panel
        message_panel = pygame.Rect(20, 540, 280, 160)  # topleft x, y, width, height
        pygame.draw.rect(screen, (44, 44, 62), message_panel, border_radius=12)
        pygame.draw.rect(screen, WHITE, message_panel, 2, border_radius=12)

        if self.active_player is not None:
            turn_text = self.game.sub_font.render(
                f"Player {self.active_player} is answering", True, WHITE
            )
            timer_text = self.game.sub_font.render(
                f"Time left: {time_left}s", True, WHITE
            )
            screen.blit(turn_text, (message_panel.x + 20, message_panel.y + 20))
            screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 60))
        else:
            wait_text = self.game.sub_font.render("Press set when ready", True, WHITE)
            screen.blit(wait_text, (message_panel.x + 20, message_panel.y + 20))

            timer_text = self.game.sub_font.render(f"Time left: {time_left}s", True, WHITE)
            screen.blit(timer_text, (message_panel.x + 20, message_panel.y + 60))