import pygame

def show_result(self):
    font = pygame.font.SysFont(None, 60)

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

        self.screen.fill((30, 30, 30))

        # winner text
        if self.winner == "P1":
            text = "Player 1 Wins"
        elif self.winner == "P2":
            text = "Player 2 Wins"
        else:
            text = "No winner"

        txt = font.render(text, True, (255, 255, 255))
        self.screen.blit(txt, txt.get_rect(center=(540, 250)))

        pygame.draw.rect(self.screen, (100, 100, 200), menu_btn)
        pygame.draw.rect(self.screen, (100, 200, 100), play_btn)

        menu_text = font.render("Menu", True, (255, 255, 255))
        play_text = font.render("Play Again", True, (255, 255, 255))

        self.screen.blit(menu_text,
                         menu_text.get_rect(center=menu_btn.center))
        self.screen.blit(play_text,
                         play_text.get_rect(center=play_btn.center))

        pygame.display.flip()
        self.clock.tick(60)