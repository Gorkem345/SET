import pygame
import sys
from screens.StartScreen import StartScreen
from screens.GameScreen import GameScreen
from screens.Rules import RulesScreen
from screens.WinnerScreen import WinnerScreen
from screens.TableDisplay import Display_card
from utils.set_table import Table
from screens.Singleplayer import SingleplayerScreen
from screens.PreStartScreen import PreStartScreen


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080, 720))
        pygame.mixer.init()

        #create font type and size
        self.font = pygame.font.SysFont("Corbel", 40)
        self.sub_font = pygame.font.SysFont("Corbel", 25)
        self.title_font = pygame.font.SysFont("Corbel", 60)
        self.small_font = pygame.font.SysFont("Corbel", 18)

        self.display_card = Display_card()
        self.table = Table()
        self.table.handle_start_game()

        #create different screens/pages
        self.start_screen = StartScreen(self) #create a startscreen instance StartScreen()
                                              # and pass self (Game object) into it
                                              #inside the StartScreen
                                              #it takes one argument - game
                                              #so now self (Startscreen).game = game (Game object)
                                              #save the Game object inside the Startscreen

        self.singleplayer_screen = SingleplayerScreen(self)
        self.game_screen = GameScreen(self)
        self.rules_screen = RulesScreen(self)
        self.winner_screen = WinnerScreen(self)
        self.pre_start_screen = PreStartScreen(self)


        self.current_screen = self.start_screen
        self.running = True
        #self.clock = pygame.time.Clock()  maybe we need to limit the FPS????

        #add winner data
        self.winner = ""
        self.p1_score = 0
        self.p2_score = 0

    def run(self):
        while self.running:
            for event in pygame.event.get(): #pygame.event is the turns the user action like pressing keys
                                             #mouse clicking, closing window into event and store in pygame
                                             #pygame.event.get() is the get all user actions since last frame
                                             #a frame is a loop, the loop can be hundreds to thousands per sec
                if event.type == pygame.QUIT:
                    self.running = False

                self.current_screen.handle_event(event)
                #self.current_screen = self.start_screen
                #self.start_screen = StartScreen(self)
                #so self.current_screen is a StartScreen object, has handle_event function

                #pass each event (mouse click, keyboard type) to handle_event

            self.current_screen.draw(self.screen)
            pygame.display.update()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Game().run() #it call run function ->while loop
                  # ->the mouse click or keyboard type will be captured and pass to handle_event function in StartScreen
