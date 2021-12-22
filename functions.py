import pygame


def load_boards():
    boards = []
    board = []
    file = open("boards.txt", "r")
    rows = file.readlines()
    i = 0
    for row in rows:
        if row[0] != "\n":
            row = row[:-1]
            board.append(list(map(int, row.split(","))))
        else:
            boards.append(board)
            board = []
            i += 1

    file.close()
    return boards


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, win):
        win.blit(self.image, (self.rect.x, self.rect.y))

    def click(self, pos):
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True
        else:
            return False


def format_time(secs):
    sec = secs % 60
    minute = secs // 60
    hour = minute // 60
    if sec < 10:
        sec = "0" + str(sec)
    else:
        sec = str(sec)
    if minute < 10:
        minute = "0" + str(minute)
    else:
        minute = str(minute)
    if hour < 10:
        hour = "0" + str(hour)
    else:
        hour = str(hour)
    mat = " " + hour + ":" + minute + ":" + sec
    return mat
