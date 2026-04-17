import pygame
import image_dictionary
from constants import WHITE, BG, DARK, LIGHT

class GameScreen:
    def __init__(self, game): #self.game_screen = GameScreen(self)
        self.game = game #game here is the Game object, so self.game = Game()

        #Player interface
        self.p1setbutton = pygame.Rect(200, 80, 100, 60)
        self.p2setbutton = pygame.Rect(200, 180, 100, 60)

        #testing button
        self.plus = pygame.Rect(500, 80, 100, 60)
        self.minus = pygame.Rect(500, 180, 100, 60)

        # -----------------------------
        # Score system
        # -----------------------------
        self.p1_score = 0 #initial score
        self.p2_score = 0

        # Which player pressed SET?
        self.active_player = None

        # Timer settings
        self.set_time_limit = 15000  # 15000 milliseconds = 15 seconds
        self.set_start_time = 0

        #Winner: Score > 30
        self.winner = None

    def start_set_timer(self, player):
        """Start the 15-second answer period for one player."""
        self.active_player = player
        self.set_start_time = pygame.time.get_ticks() #it is the time pass when the game start until you click SET button
        #a = f'set_start_time: {self.set_start_time}'
        #print(a)


    def clear_set_timer(self):
        """Stop the answer period."""
        self.active_player = None
        self.set_start_time = 0

    def get_time_left(self):
        """Return remaining time in seconds. If no timer, return 15''."""

        if self.active_player is None:
            return "%d" % 15

        current_time = pygame.time.get_ticks() #what is the time now (from game start until now)
        #print(f'current time: {current_time}')

        elapsed =  current_time - self.set_start_time #the time now - the time you click the SET button
                                                      #it is the time passed after you click the SET button
        remaining = self.set_time_limit - elapsed

        if remaining <= 0:
            self.clear_set_timer()
            return 0

        return remaining // 1000 + 1 #15 + 1 to make sure the count down start from 15s instead of 14

    def check_winner(self):
        #GameScreen knows Game
        #WinnerScreen knows Game
        #WinnerScreen does not know Gamescreen
        #in this case you need self.game (Game object), store the score and winner
        #as an attribute of Game object so that it can access to WinnerScreen

        if self.p1_score >= 30:
            self.game.winner = "Player 1!"
            self.game.p1_score = self.p1_score
            self.game.p2_score = self.p2_score
            self.game.current_screen = self.game.winner_screen

            # reset timer, player and score
            self.clear_set_timer()
            self.p1_score = 0  # initial score
            self.p2_score = 0

        elif self.p2_score >= 30:
            self.game.winner = "Player 2!"
            self.game.p1_score = self.p1_score
            self.game.p2_score = self.p2_score
            self.game.current_screen = self.game.winner_screen

            # reset timer, player and score
            self.clear_set_timer()
            self.p1_score = 0  # initial score
            self.p2_score = 0

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()  # get mouse position

        if event.type == pygame.MOUSEBUTTONDOWN:  # if mouse was clicked
            if self.p1setbutton.collidepoint(mouse):  # if the mouse is clicked inside the play button area
                if self.active_player is None: #other SET button cannot be activated
                    self.start_set_timer(1)

            # Click on Quit --> shut down
            elif self.p2setbutton.collidepoint(mouse):
                if self.active_player is None:
                    self.start_set_timer(2)

            # PLUS button
            elif self.plus.collidepoint(mouse):
                if self.active_player == 1:
                    self.p1_score += 1
                    self.check_winner()

                elif self.active_player == 2:
                    self.p2_score += 1
                    self.check_winner()

            # MINUS button
            elif self.minus.collidepoint(mouse):
                if self.active_player == 1:
                    self.p1_score -= 1
                    self.check_winner()

                elif self.active_player == 2:
                    self.p2_score -= 1
                    self.check_winner()


    def draw(self, screen): #screen here is the self.screen from Game
        mouse = pygame.mouse.get_pos()
        screen.fill(BG)

        # Check timer every frame
        time_left = self.get_time_left()

        # Scoreboard
        p1_score_text = self.game.sub_font.render(f"P1 Score: {self.p1_score}",
                                                  True, WHITE)
        p2_score_text = self.game.sub_font.render(f"P2 Score: {self.p2_score}",
                                                  True, WHITE)

        screen.blit(p1_score_text, (100, 140))
        screen.blit(p2_score_text, (100, 240))

        #p1, p2 label position
        p1_text = self.game.sub_font.render("Player 1", True, WHITE)
        p1_rect = p1_text.get_rect(topleft=(100, 100))
        screen.blit(p1_text, p1_rect)
        p2_text = self.game.sub_font.render("Player 2", True, WHITE)
        p2_rect = p2_text.get_rect(topleft=(100, 200))
        screen.blit(p2_text, p2_rect)

        #p1, p2 set button text
        p1set_text = self.game.sub_font.render("SET", True, WHITE)
        p2set_text = self.game.sub_font.render("SET", True, WHITE)

        #Place p1, p2 set button
        pygame.draw.rect(screen, LIGHT if self.p1setbutton.collidepoint(
            mouse) else DARK, self.p1setbutton)
        screen.blit(p1set_text, p1set_text.get_rect(
            center=(self.p1setbutton.centerx, self.p1setbutton.centery)))
            #p1set_text.get_rect(), create a rectangle for that text, position it use center = (x, y)
            #self.p1setbutton.centerx,  horizontally: center of the button

        pygame.draw.rect(screen, LIGHT if self.p2setbutton.collidepoint(
            mouse) else DARK, self.p2setbutton)
        screen.blit(p2set_text, p2set_text.get_rect(
            center=(self.p2setbutton.centerx, self.p2setbutton.centery)))

        # testing button
        plus_text = self.game.sub_font.render("PLUS", True, WHITE)
        minus_text = self.game.sub_font.render("MINUS", True, WHITE)
        pygame.draw.rect(screen, LIGHT if self.plus.collidepoint(
            mouse) else DARK, self.plus)
        screen.blit(plus_text, plus_text.get_rect(
            center=(self.plus.centerx, self.plus.centery)))
        pygame.draw.rect(screen, LIGHT if self.minus.collidepoint(
            mouse) else DARK, self.minus)
        screen.blit(minus_text, minus_text.get_rect(
            center=(self.minus.centerx, self.minus.centery)))

# -----------------------------
        # Show whose turn it is
        # -----------------------------
        if self.active_player is not None:
            turn_text = self.game.sub_font.render(
                f"Player {self.active_player} is answering",
                True,
                WHITE
            )
            screen.blit(turn_text, (700, 100))

            timer_text = self.game.sub_font.render(
                f"Time left: {time_left}s",
                True,
                WHITE
            )
            screen.blit(timer_text, (700, 150))
        else:
            wait_text = self.game.sub_font.render(
                "No active SET call",
                True,
                WHITE
            )
            screen.blit(wait_text, (700, 100))





