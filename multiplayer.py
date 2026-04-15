import pygame

font = pygame.font.SysFont("Corbel", 40)
WHITE = (255, 255, 255)

def game(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" # Tell main.py to quit
            # Example: Press ESC to go back to the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"

        screen.fill((40, 40, 40))

        text = font.render("Game Started! Press ESC to go back.", True, WHITE)
        screen.blit(text, (250, 350))

        pygame.display.update()