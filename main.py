import pygame
import sys

#import scripts
import StartScreenTest
import multiplayer




# 1. Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1080, 720))
pygame.display.set_caption("Set Card Game")


def main():
    # Keep track of which screen we are on
    current_state = "MENU"
    winner = None

    while True:
        # The traffic cop logic
        if current_state == "MENU":
            # Pass the screen to the menu, and wait for it to return the next state
            current_state = StartScreenTest.start_menu(screen)

        elif current_state == "GAME":
            # Pass the screen to the game, and wait for it to return the next state
            current_state, winner = multiplayer.game(screen)

        elif current_state == "RESULT":
            current_state = show_result(screen, winner)

        elif current_state == "QUIT":
            pygame.quit()
            sys.exit()


def show_result(screen, winner):
    font = pygame.font.SysFont(None, 60)
    clock = pygame.time.Clock()

    # buttons
    menu_btn = pygame.Rect(300, 450, 200, 80)
    play_btn = pygame.Rect(580, 450, 200, 80)

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"

            if event.type == pygame.MOUSEBUTTONDOWN:
                if menu_btn.collidepoint(event.pos):
                    return "MENU"
                if play_btn.collidepoint(event.pos):
                    return "GAME"

        screen.fill((30, 30, 30))

        # winner text
        if winner == "P1":
            text = "Player 1 Wins"
        elif winner == "P2":
            text = "Player 2 Wins"
        else:
            text = "No winner"

        txt = font.render(text, True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=(540, 250)))

        # draw buttons
        pygame.draw.rect(screen, (100, 100, 200), menu_btn)
        pygame.draw.rect(screen, (100, 200, 100), play_btn)

        # hover effect (optional)
        if menu_btn.collidepoint(mouse):
            pygame.draw.rect(screen, (255, 255, 255), menu_btn, 3)
        if play_btn.collidepoint(mouse):
            pygame.draw.rect(screen, (255, 255, 255), play_btn, 3)

        # button text
        menu_text = font.render("Menu", True, (255, 255, 255))
        play_text = font.render("Play Again", True, (255, 255, 255))

        screen.blit(menu_text, menu_text.get_rect(center=menu_btn.center))
        screen.blit(play_text, play_text.get_rect(center=play_btn.center))

        pygame.display.flip()
        clock.tick(60)



# Start the program
if __name__ == "__main__":
    main()