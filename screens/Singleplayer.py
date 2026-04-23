import pygame
from utils.constants import WHITE, DARK, LIGHT
from screens.TableDisplay import Display_board
from utils.set_table import Table
import random
from screens.PlayScreen import PlayScreen


class SingleplayerScreen(PlayScreen):
    '''
    Description:
    Manages the single-player game mode against a computer AI opponent. Inherits foundational UI and timer logic from `PlayScreen`. It handles human vs. computer scoring, rendering the specific single-player layout, and driving the computer's "thinking" and "clicking" state machine (including simulated human-like delays and intentional mistakes based on difficulty).
    Parameters:
    game: The main Game object acting as the application controller.
    Limitations:
    The AI's "mistakes" are chosen by picking completely random cards, rather than picking visually similar cards that a human might accidentally confuse.
    Structures:
    Inherits from `PlayScreen`. Utilizes `pygame.time.get_ticks()` for asynchronous AI state management, integer lists to queue the AI's clicks, and random number generation for difficulty scaling.
    Outputs:
    An active SingleplayerScreen object ready to be assigned to the game's main loop.
    '''
    def __init__(self, game):  # self.game_screen = GameScreen(self)
        '''
        Description:
        Initializes the single-player environment, calling the parent setup and establishing computer-specific variables
        like independent scores, AI timers, and difficulty settings.
        Parameters:
        game: The main Game object.
        Limitations:
        Default difficulty is hardcoded to "Normal" upon initialization.
        Structures:
        Calls `super().__init__(game)`. Sets up an empty list `comp_clicks_pending` to act as a queue for the AI's
        automated card clicks.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Completely resets the single-player specific data (scores, computer timers, and queued AI clicks) alongside the
        base UI and table resets from the parent class, preparing a fresh match.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Calls `super().reset_game_screen()`. Zeros out integer scores and empties the `comp_clicks_pending` array.
        Outputs:
        None.
        '''
        super().reset_game_screen()
        self.p1_score = 0
        self.comp_score = 0

        # Completely Reset the Computer
        self.reset_computer_timer()  # Give it a fresh 8-20 seconds
        self.comp_clicks_pending = []  # Clear any queued clicks


    def clear_set_timer(self):
        '''
        Description:
        Stops the 15-second active answering timer via the parent class, and simultaneously resets the computer's
        hidden timer so it can begin "thinking" about its next move.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Calls `super().clear_set_timer()` and executes `self.reset_computer_timer()`.
        Outputs:
        None.
        '''
        super().clear_set_timer()
        self.reset_computer_timer()

    def resume_game_timer(self):
        '''
        Description:
        Unpauses the game, ensuring that both the global game timer and the computer's internal target time are pushed
        forward to account for the time spent paused.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Calculates the paused duration and adds it to `self.game_start_time` and `self.comp_target_time`.
        Outputs:
        None.
        '''
        if self.paused:
            paused_duration = pygame.time.get_ticks() - self.pause_start_time
            self.game_start_time += paused_duration
            self.comp_target_time += paused_duration
            self.paused = False


    def check_game_timeout(self):
        '''
        Description:
        Monitors the global game timer. If time expires, it forces an end-game state, determines the winner between the
        human and AI based on current scores, and transitions the game to the WinnerScreen.
        Parameters:
        None.
        Limitations:
        -
        Structures:
        Uses basic if/elif comparison logic. Mutates attributes on the central `self.game` object to pass data to the
        WinnerScreen.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Monitors the table state. If there are no possible SETs left in the deck/table, it ends the game, calculates
        the winner between the player and computer, updates global state, and navigates to the WinnerScreen.
        Parameters:
        None.
        Limitations:
        Relying on `self.game.table.find_sets()` being empty assumes the `Table` class has accurately exhausted all
        reshuffling attempts.
        Structures:
        If/elif conditions for score comparison, followed by global state mutation and a screen routing change.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Calculates a randomized future timestamp (`comp_target_time`) dictating when the computer will attempt to find
        and claim a SET. The delay scales based on the current difficulty setting.
        Parameters:
        None.
        Limitations:
        Hardcoded integer bounds for the randomization ranges.
        Structures:
        Evaluates `self.difficulty` strings ("Easy", "Normal", "Hard") to pick a bound, then uses `random.randint`
        added to `pygame.time.get_ticks()`.
        Outputs:
        None.
        '''
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
        '''
        Description:
        The core AI state machine. Evaluates whether the computer is "clicking" (processing queued card selections with
        human-like visual delays) or "thinking" (waiting for its timer to expire). It occasionally injects intentional mistakes into the computer's clicks based on difficulty probability.
        Parameters:
        None.
        Limitations:
        Because mistakes are generated using entirely random board indices, the AI's "mistakes" often look completely
        illogical to a human player, rather than being "close" misses.
        Structures:
        Operates on current millisecond ticks. Uses `list.pop(0)` to process queued clicks. Calculates mistake
        probabilities using `random.randint(1, a)` where `a` varies by difficulty.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Intercepts user inputs specific to the Singleplayer screen. Processes the human player pressing Spacebar to
        claim a turn, clicking UI buttons, and selecting cards on the table while explicitly blocking human card selection during the computer's turn.
        Parameters:
        event (pygame.event.Event): The Pygame event object triggered by keyboard or mouse actions.
        Limitations:
        Heavily nested logic structure. Requires precise mapping between the mouse collision points and the visual
        boundaries defined in the parent class.
        Structures:
        Branches based on `event.type`. Uses `pygame.Rect.collidepoint` for button presses and queries
        `self.board.get_clicked_card_index` for board interactions. Directly invokes scoring arithmetic and audio feedback on successful/failed SETs.
        Outputs:
        None.
        '''
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
        '''
        Description:
        Renders the comprehensive visual state of the Singleplayer mode. Responsible for drawing the background,
        prompting the computer logic to update, rendering the playing board, and formatting the UI panels (scores,
        remaining cards, timers, buttons, and dynamic status messaging).
        Parameters:
        screen (pygame.Surface): The primary display surface window where graphics are blitted.
        Limitations:
        Coordinates, box sizes, and padding offsets are hardcoded, relying on Pygame's SCALED environment to adapt to
        various monitors.
        Structures:
        Calls `update_computer()` before drawing. Uses `pygame.draw.rect` for styling panels/buttons and
        `self.game.font.render` for text. Derives hover-states dynamically by comparing `pygame.mouse.get_pos()`
        against the parent UI Rects.
        Outputs:
        Refreshes the visual output on the provided screen Surface.
        '''
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