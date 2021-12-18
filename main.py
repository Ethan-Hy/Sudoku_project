import pygame


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku")

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        win.fill((255, 255, 255))
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()