import numpy as np
import pygame
import time


COLOR_BACKGROUND = (45, 20, 90)
COLOR_GRID = (80, 20, 90)
NEXT_DIE = (110, 180, 120)
NEXT_LIVE = (150, 155, 105)

def update(screen, cells, size, with_progress=False):
    updated_cells = np.zeros((cells.shape[0], cells.shape[1]))

    for row, col in np.ndindex(cells.shape):
        alive = np.sum(cells[row-1:row+2, col-1:col+2]) - cells[row, col]
        color = COLOR_BACKGROUND if cells[row, col] == 0  else NEXT_LIVE
        
        if cells[row, col] == 1:
            if alive < 2 or alive > 3:
                if with_progress:
                    color = NEXT_DIE
            elif 2 <= alive <= 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = NEXT_LIVE
        else:
            if alive == 3:
                updated_cells[row, col] = 1
                if with_progress:
                    color = NEXT_LIVE
        
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size -1))

    return updated_cells

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    shape = 60, 80
    cells = np.zeros(shape)
    screen.fill(COLOR_GRID)
    update(screen, cells, 10)

    pygame.display.flip()
    pygame.display.update()

    running = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    running = not running
                    update(screen, cells, 10)
                    pygame.display.update()
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                cells[pos[1] // 10, pos[0] // 10] = 1
                update(screen, cells, 10)
                pygame.display.update()

        screen.fill(COLOR_GRID)
        if running:
            cells = update(screen, cells, 10, with_progress=True)
            pygame.display.update()

        time.sleep(1)

if __name__ == '__main__':
    main()
