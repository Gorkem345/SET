import pygame

WHITE = (255,255,255)
LIGHT = (170,170,170)
DARK = (100,100,120)
BG = (60, 25, 100)

pygame.font.init()
font = pygame.font.SysFont("Corbel", 40)
sub_font = pygame.font.SysFont("Corbel", 25)


def start_menu(screen):
    logo_image = pygame.image.load("images/set_cards.png").convert_alpha()

    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        title_font = pygame.font.SysFont("Corbel", 60)
        title_text = title_font.render("Welcome to the game Set", True, WHITE)
        title_rect = title_text.get_rect(center=(1080 // 2, 80))
        screen.blit(title_text, title_rect)

        play_button = pygame.Rect(470, 310, 140, 80)
        quit_button = pygame.Rect(470, 410, 140, 50)
        rules_button = pygame.Rect(0, 600, 140, 50)

        pygame.draw.rect(screen, LIGHT if play_button.collidepoint(mouse) else DARK, play_button)
        pygame.draw.rect(screen, LIGHT if quit_button.collidepoint(mouse) else DARK, quit_button)
        pygame.draw.rect(screen, LIGHT if rules_button.collidepoint(mouse) else DARK, rules_button)

        play_text = font.render("Play", True, WHITE)
        play_subtext = sub_font.render("2 Players", True, WHITE)
        quit_text = font.render("Quit", True, WHITE)
        rules_text = font.render("Rules", True, WHITE)

        screen.blit(play_text, play_text.get_rect(center=(play_button.centerx, play_button.centery - 15)))
        screen.blit(play_subtext, play_subtext.get_rect(center=(play_button.centerx, play_button.centery + 20)))
        screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))
        screen.blit(rules_text, rules_text.get_rect(center=rules_button.center))

        rect = logo_image.get_rect(center=(1080 // 2, 200))
        screen.blit(logo_image, rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.collidepoint(mouse):
                    return "GAME"
                if quit_button.collidepoint(mouse):
                    return "QUIT"
        pygame.display.update()