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

    #new part
    clock = pygame.time.Clock()

    # two buttons
    left_btn = pygame.Rect(180, 550, 250, 80)
    right_btn = pygame.Rect(650, 550, 250, 80)

    while True:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT", None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "MENU", None

            if event.type == pygame.MOUSEBUTTONDOWN:
                if left_btn.collidepoint(event.pos):
                    return "RESULT", "P1"
                if right_btn.collidepoint(event.pos):
                    return "RESULT", "P2"

        screen.fill((40, 40, 40))

        screen.blit(dummy_card, (0, 0))

        text = font.render("Click a button to choose winner", True, WHITE)
        screen.blit(text, (250, 350))

        # draw buttons
        pygame.draw.rect(screen, (170, 100, 100), left_btn)
        pygame.draw.rect(screen, (100, 170, 100), right_btn)

        # optional hover effect
        if left_btn.collidepoint(mouse):
            pygame.draw.rect(screen, WHITE, left_btn, 3)
        if right_btn.collidepoint(mouse):
            pygame.draw.rect(screen, WHITE, right_btn, 3)

        left_text = font.render("Player 1 Wins", True, WHITE)
        right_text = font.render("Player 2 Wins", True, WHITE)

        screen.blit(left_text, left_text.get_rect(center=left_btn.center))
        screen.blit(right_text, right_text.get_rect(center=right_btn.center))

        pygame.display.update()
        clock.tick(60)



'''
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

'''
