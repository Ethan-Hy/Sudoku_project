import pygame
from solver import valid, solve, find_next
from functions import load_boards, Button, format_time
import time
pygame.init()

FONT_SIZE = 45
FONT = "calibri"
WIDTH = 540
HEIGHT = 640
DIFFICULTIES = ["Easy", "Normal", "Hard"]
DIFFICULTY = 0

# boards taken from https://sudoku.com/
BOARDS = load_boards()

# load button image and create instance
button_magic_img = pygame.image.load("button2.png")
button_magic = Button(WIDTH/2 - 100, WIDTH + 20, button_magic_img, 0.7)
button_arrow_r_img = pygame.image.load("arrow.png")
button_arrow_l_img = pygame.transform.flip(button_arrow_r_img, True, False)
button_arrow_r = Button(WIDTH - 82, WIDTH + 72, button_arrow_r_img, 0.2)
button_arrow_l = Button(WIDTH - 100, WIDTH + 72, button_arrow_l_img, 0.2)


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
        # font_temp = pygame.font.SysFont(FONT, round(FONT_SIZE * 0.7))
        # space for each box on a grid
        space = self.width / 9
        # starting point of box on the grid
        x = self.col * space
        y = self.row * space

        # highlight box when selected
        if self.selected:
            pygame.draw.rect(win, (200, 0, 0), (x, y, space, space), 6)

        # change values
        # temporary value in top left corner when value hasn't been submitted yet
        if self.temp != 0 and self.value == 0:
            text = font.render(str(self.temp), 1, (128, 0, 0))
            win.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))
        # value submitted
        elif self.value != 0:
            text = font.render(str(self.value), 1, (0, 0, 0))
            win.blit(text, (x + (space / 2 - text.get_width() / 2), y + (space / 2 - text.get_height() / 2)))


class Grid:

    def __init__(self, board, rows, cols, width, height):
        self.board = board
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
            if valid(self.model, (row, col), val) and solve(self.model):
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
        space = self.width / 9

        # highlight grid when a box is selected
        if self.selected:
            row, col = self.selected
            pygame.draw.rect(win, (173, 216, 230),
                             ((col // 3) * 3 * space, (row // 3) * 3 * space, 3 * space, 3 * space))
            pygame.draw.rect(win, (173, 216, 230), (col * space, 0, space, 9 * space))
            pygame.draw.rect(win, (173, 216, 230), (0, row * space, 9 * space, space))

        # Draw Grid Lines
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
            return int(x), int(y)
        else:
            return None

    # check if sudoku is completed by detecting whether any empty boxes remain
    def completed(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.boxes[i][j].value == 0:
                    return False
        return True


# solve the sudoku automatically
def auto_solve(boa, win, board, play_time, lives, difficulty):
    # clear events so program does not get disturbed during auto_solve
    pygame.event.clear()
    find = find_next(boa.model)

    if not find:
        return True
    else:
        boa.select(find[0], find[1])
        x, y = find
        for i in range(1, len(boa.model) + 1):
            if valid(boa.model, (x, y), i):
                boa.boxes[x][y].set(i)
                boa.update_model()
                redraw_window(win, board, play_time, lives, difficulty)
                pygame.display.update()
                pygame.time.delay(5)
                if auto_solve(boa, win, board, play_time, lives, difficulty):
                    return True
                # if it cannot solve backtrack - recursion
                boa.select(x, y)
                redraw_window(win, board, play_time, lives, difficulty)
                pygame.display.update()
                boa.boxes[x][y].set(0)
                boa.update_model()
                redraw_window(win, board, play_time, lives, difficulty)
                pygame.display.update()
                pygame.time.delay(5)
        return False


def redraw_window(win, board, time, lives, difficulty):
    # background colour
    win.fill((255, 254, 234))
    # Draw time
    font = pygame.font.SysFont(FONT, round(FONT_SIZE * 0.8))
    font_small = pygame.font.SysFont(FONT, round(FONT_SIZE * 0.4))
    text = font.render("Time: " + format_time(time), 1, (0, 0, 0))
    win.blit(text, (WIDTH - 240, WIDTH + 30))
    # Draw number of lives
    text = font.render("Lives: " + str(lives), 1, (200, 0, 0))
    win.blit(text, (20, WIDTH + 30))
    # Draw grid and board
    board.draw(win)
    # Draw buttons
    button_magic.draw(win)
    button_arrow_r.draw(win)
    button_arrow_l.draw(win)
    # Draw on restart instruction
    text = font_small.render("Press R to restart", 1, (0, 0, 0))
    win.blit(text, (20, HEIGHT - 30))
    # Draw difficulty
    text = font_small.render("Difficulty: " + DIFFICULTIES[difficulty], 1, (0, 0, 0))
    win.blit(text, (WIDTH - 240, WIDTH + 70))


def main():
    global DIFFICULTY
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Sudoku - Ethan Hy")
    board = Grid(BOARDS[DIFFICULTY], 9, 9, WIDTH, WIDTH)
    run = True
    start = time.time()
    lives = 3
    key = None
    finished = False
    game_over = False
    auto_solved = False

    while run:
        play_time = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    main()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if button_arrow_r.click(pos):
                    if DIFFICULTY != len(DIFFICULTIES) - 1:
                        DIFFICULTY += 1
                        main()
                if button_arrow_l.click(pos):
                    if DIFFICULTY != 0:
                        DIFFICULTY -= 1
                        main()

            if not finished:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if board.click(pos):
                        board.select(board.click(pos)[1], board.click(pos)[0])
                        key = None
                    if button_magic.click(pos):
                        board.update_model()
                        pygame.event.pump()
                        auto_solve(board, win, board, play_time, lives, DIFFICULTY)
                        finished = True
                        finish_time = play_time
                        auto_solved = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_0:
                        key = 0
                    if event.key == pygame.K_1:
                        key = 1
                    if event.key == pygame.K_2:
                        key = 2
                    if event.key == pygame.K_3:
                        key = 3
                    if event.key == pygame.K_4:
                        key = 4
                    if event.key == pygame.K_5:
                        key = 5
                    if event.key == pygame.K_6:
                        key = 6
                    if event.key == pygame.K_7:
                        key = 7
                    if event.key == pygame.K_8:
                        key = 8
                    if event.key == pygame.K_9:
                        key = 9
                    if event.key == pygame.K_DELETE:
                        board.delete()
                        key = None
                    if event.key == pygame.K_RETURN:
                        i, j = board.selected
                        if board.boxes[i][j].temp != 0:
                            if board.submit(board.boxes[i][j].temp):
                                print("Correct!")
                            elif not board.submit(board.boxes[i][j].temp) and board.boxes[i][j].value == 0:
                                print("Incorrect!")
                                lives -= 1
                                if lives < 0:
                                    finished = True
                                    finish_time = play_time
                                    game_over = True
                            key = None
                            if board.completed():
                                print("Sudoku completed!")
                                finished = True
                                finish_time = play_time

        if board.selected and key != None:
            board.note(key)

        if not finished:
            redraw_window(win, board, play_time, lives, DIFFICULTY)
            pygame.display.update()
        elif finished and game_over:
            redraw_window(win, board, finish_time, lives, DIFFICULTY)
            font = pygame.font.SysFont(FONT, FONT_SIZE)
            text = font.render("Game Over", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_x = win.get_width() / 2 - text_rect.width / 2
            text_y = win.get_height() / 2 - text_rect.height / 2
            pygame.draw.rect(win, (255, 0, 0), (text_x, text_y, text_rect.width, text_rect.height))
            win.blit(text, [text_x, text_y])
            pygame.display.update()
        elif finished:
            redraw_window(win, board, finish_time, lives, DIFFICULTY)
            font = pygame.font.SysFont(FONT, FONT_SIZE)
            # text = font.render("Sudoku Completed! Your time was: " + format_time(finish_time), True, (0, 0, 0))
            if auto_solved:
                text = font.render("Magic!", True, (0, 0, 0))
            else:
                text = font.render("Sudoku Completed!", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_x = win.get_width() / 2 - text_rect.width / 2
            text_y = win.get_height() / 2 - text_rect.height / 2
            pygame.draw.rect(win, (0, 255, 0), (text_x, text_y, text_rect.width, text_rect.height))
            win.blit(text, [text_x, text_y])
            pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
