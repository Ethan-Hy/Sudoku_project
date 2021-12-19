import pygame
from solver import valid, solve
import time
pygame.init()


FONT_SIZE = 45
FONT = "arial"

class Box:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val

    # draw the boxes - highlight when selected and show numbers
    def draw(self, win):
        font = pygame.font.SysFont(FONT, FONT_SIZE)

        # space for each box on a grid
        space = self.width / 9
        # starting point of box on the grid
        x = self.col * space
        y = self.row * space

        # highlight box when selected
        if self.selected:
            pygame.draw.rect(win, (255, 0, 0), (x, y, space, space), 3)

        # change values
        # temporary value in top left corner when value hasn't been submitted yet
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 128, 128))
            win.blit(text, (x + 10, y + 10))
        # value submitted
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))


class Grid:
    board = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7]
    ]

    def __init__(self, rows, cols, width, height):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.boxes = [[Box(self.board[i][j], i, j, width, height) for j in range(cols)] for i in range(rows)]
        self.model = None
        self.selected = None

    # select the box
    def select(self, row, col):
        # Initialise by unselecting all boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].selected = False

        # select the box
        self.boxes[row][col].selected = True
        self.selected = (row, col)

    # update the box values in the board model
    def update_model(self):
        self.model = [[self.boxes[i][j].value for j in range(self.cols)] for i in range(self.rows)]

    # submit the value into box
    def submit(self, val):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set(val)
            self.update_model()

            # check if the entry is currently valid and the correct number for end solution
            if valid(self.model, val, (row, col)) and solve(self.model):
                return True
            else:
                self.boxes[row][col].set(0)
                self.boxes[row][col].set_temp(0)
                self.update_model()
                return False

    # temporary note of value of a box
    def note(self, val):
        row, col = self.selected
        self.boxes[row][col].set_temp(val)

    # draw the Grid with numbers in each box
    def draw(self, win):
        # Draw Grid Lines
        space = self.width / 9
        for i in range(self.rows + 1):
            if i % 3 == 0 and i != 0:
                line_width = 4
            else:
                line_width = 1
            pygame.draw.line(win, (0, 0, 0), (0, i * space), (self.width, i * space), line_width)
            pygame.draw.line(win, (0, 0, 0), (i * space, 0), (i * space, self.height), line_width)

        # Draw Boxes
        for i in range(self.rows):
            for j in range(self.cols):
                self.boxes[i][j].draw(win)

    # delete number in box
    def delete(self):
        row, col = self.selected
        if self.boxes[row][col].value == 0:
            self.boxes[row][col].set_temp(0)

    # click returns top left corner of box
    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            space = self.width / 9
            x = pos[0] // space
            y = pos[1] // space
            return int(y), int(x)
        else:
            return None

    # check if sudoku is completed by detecting whether any empty boxes remain
    def completed(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True




def redraw_window(win, board, time, strikes):
    # white background
    win.fill((255, 255, 255))
    # Draw time
    font = pygame.font.SysFont(FONT, FONT_SIZE)
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (540 - 160, 560))
    # Draw number of strikes
    text = font.render("Strikes: " + str(strikes), 1, (255, 0, 0))
    win.blit(text, (20, 560))
    # Draw grid and board
    board.draw(win)


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60

    mat = " " + str(hour) + ":" + str(minute) + ":" + str(sec)
    return mat


def main():
    win = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Sudoku - Ethan Hy")
    board = Grid(9, 9, 540, 540)
    run = True
    start = time.time()
    strikes = 0

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        redraw_window(win, board, play_time, strikes)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()