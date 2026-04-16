import pygame
import image_dictionary

pygame.display.init()
pygame.font.init()

font = pygame.font.SysFont("Corbel", 40)
WHITE = (255, 255, 255)



def game(screen):
    sheet = pygame.image.load("images/cover.png").convert()

    id = "srs3" #Try different IDs to test
    card_rect = pygame.Rect(image_dictionary.cards[id].coordinates[0], image_dictionary.cards[id].coordinates[1],
                            image_dictionary.cards[id].coordinates[2], image_dictionary.cards[id].coordinates[3])
    dummy_card = sheet.subsurface(card_rect)

    dummy_card = pygame.transform.scale(dummy_card, (image_dictionary.cards[id].coordinates[2] * 2, image_dictionary.cards[id].coordinates[3] * 2))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT" # Tell main.py to quit
            # Example: Press ESC to go back to the menu
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU"


        screen.fill((40, 40, 40))

        screen.blit(dummy_card, (0, 0))

        text = font.render("Game Started! Press ESC to go back.", True, WHITE)
        screen.blit(text, (250, 350))

        pygame.display.update()