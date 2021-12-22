def load_boards():
    boards = []
    board = []
    file = open("boards.txt", "r")
    rows = file.readlines()
    i = 0
    print(rows)
    for row in rows:
        if row[0] != "\n":
            row = row[:-1]
            board.append(list(map(int, row.split(","))))
        else:
            boards.append(board)
            print(board)
            board = []
            i += 1

    file.close()
    return boards


load_boards()