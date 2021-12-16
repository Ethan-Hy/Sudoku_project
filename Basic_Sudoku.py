# initial basic Sudoku solver
# use back tracking algorithm
board = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def print_board(board):
    # i is row
    for i in range(len(board)):
        # j is column
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(board[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end='')
            if j == len(board[0]) - 1:
                print(board[i][j])
            else:
                print(str(board[i][j]) + ' ', end='')


# find the next empty position in the board
# go from left to right, top to bottom
def find_next(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None

# determine if input is valid
# position inputted is (row, column)
def valid(board, position, number):

    # check row so go through columns of the row
    for j in range(len(board[0])):
        if board[position[0]][j] == number and j != position[1]:
            return False

    # check column so go through rows of the column
    for i in range(len(board)):
        if board[i][position[1]] == number and i != position[0]:
            return False

    # check 3x3 box
    # have each box represented by (x, y) position
    x = position[0] // 3
    y = position[1] // 3
    for i in range(3):
        for j in range(3):
            if board[3 * x + i][3 * y + j] == number and (i, j) != position:
                return False

    return True

# solve the Sudoku
# use backtracking algorithm




print_board(board)

# print(valid(board, find_next(board), 3))

