import pygame
import sys
import StartScreenTest
import multiplayer

# 1. Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Set Card Game")


def main():
    # Keep track of which screen we are on
    current_state = "MENU"

    while True:
        # The traffic cop logic
        if current_state == "MENU":
            # Pass the screen to the menu, and wait for it to return the next state
            current_state = StartScreenTest.start_menu(screen)

        elif current_state == "GAME":
            # Pass the screen to the game, and wait for it to return the next state
            current_state = multiplayer.game(screen)

        elif current_state == "QUIT":
            pygame.quit()
            sys.exit()


# Start the program
if __name__ == "__main__":
    main()