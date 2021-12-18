# initial basic Sudoku solver
# use back tracking algorithm

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


# board = [
#     [5,1,6,8,4,9,7,3,2],
#     [3,0,7,6,0,5,0,0,0],
#     [8,0,9,7,0,0,0,6,5],
#     [1,3,5,0,6,0,9,0,7],
#     [4,7,2,5,9,1,0,0,6],
#     [9,6,8,3,7,0,0,5,0],
#     [2,5,3,1,8,6,0,7,4],
#     [6,8,4,2,0,7,5,0,0],
#     [7,9,1,0,5,0,6,0,8]
# ]

def print_board(boa):
    # i is row
    for i in range(len(boa)):
        # j is column
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - -")
        for j in range(len(boa[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end='')
            if j == len(boa[0]) - 1:
                print(boa[i][j])
            else:
                print(str(boa[i][j]) + ' ', end='')


# find the next empty position in the board
# go from left to right, top to bottom
def find_next(boa):
    for i in range(len(boa)):
        for j in range(len(boa[0])):
            if boa[i][j] == 0:
                return i, j
    return None


# determine if input is valid
# position inputted is (row, column)
def valid(boa, position, number):
    # check row so go through columns of the row
    for j in range(len(boa[0])):
        if boa[position[0]][j] == number and j != position[1]:
            return False

    # check column so go through rows of the column
    for i in range(len(boa)):
        if boa[i][position[1]] == number and i != position[0]:
            return False

    # check 3x3 box
    # have each box represented by (x, y) position
    x = position[0] // 3
    y = position[1] // 3
    for i in range(3):
        for j in range(3):
            if boa[3 * x + i][3 * y + j] == number and (i, j) != position:
                return False

    return True


# solve the Sudoku
# use backtracking algorithm
def solve(boa):

    find = find_next(boa)
    # base case where board is full
    if not find:
        return True
    else:
        x, y = find
        # try out each possibility
        for i in range(1, len(boa) + 1):
            if valid(boa, (x, y), i):
                boa[x][y] = i
                # print_board(boa)
                if solve(boa):
                    return True
                # if it cannot solve backtrack - recursion
                boa[x][y] = 0
                # print_board(boa)
        return False


print_board(board)
if not solve(board):
    print("Not solvable!")
else:
    print("-----------------------------------")
    print_board(board)
    # print(valid(board, find_next(board), 3))
