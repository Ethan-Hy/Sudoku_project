# Sudoku Game with Auto-solve - Ethan Hy
#### Video Demo:  https://youtu.be/1p5CYge4_rk
#### Description:
This pygame app is a Sudoku game where you can play Sudoku normally and auto-solve it using the Magic button.
There is a timer and you have 3 lives, once you go below 0 lives you lose and must restart.

#### File Structure:
The `Basic_Sudoku.py` script is the initial script made to solve the Sudoku board automatically using a back tracking algorithm.

The functions used to create `Basic_Sudoku.py` are then put into `solver.py` which are to be used in this app.

General functions are then put into `functions` which include a file reading function to input boards from a text file, an interactive pygame button, and a time formatting function.

The main app is built in `Sudoku.py`. Two Classes are made, a  `Box` Class which is inherited by the `Grid` Class which are used to construct the Sudoku board. 
The `auto_solve` function is made here using functions from `solver.py` where each number submission is animated to show the user how the back tracking algorithm works. Initially a time delay was introduced (which is currently commented out)
to show the back tracking algorithm more clearly, however, the current Sudoku puzzles being used can take some time to solve so it has been commented out. Instructions are below to reintroduce this time delay.

#### Instructions for Use:
To launch, open `Sudoku.exe` within the main folder.

To play, click on an empty box and type in a number to sketch it in red. To submit a number, press enter whilst the box is selected.
If the number is incorrect you lose a life. 

If all the boxes are filled in then you have solved the Sudoku.

To restart the game press R on your keyboard.

On initial launch, the game starts off with an "Easy" difficulty board. You can change the difficulty by clicking on the arrows to navigate between Easy, Normal and Hard difficulties.

When the Magic button is clicked, the Sudoku is solved using a back tracking algorithm and animates each number submission.
If you wish to see this algorithm more clearly, you can introduce a delay between animated submissions in the code by uncommenting the following in `Sudoku.py`: `# pygame.time.delay(AUTO_DELAY)` within the `auto_solve` function.
Note that this will not change the .exe file and you will need to use an interpreter to run `Sudoku.py` or use pyinstaller with the command `pyinstaller --onefile Sudoku.py` to recreate the `Sudoku.exe` file. Ensure the  `Sudoku.exe` file is in the main folder and not in dist.

If you wish to use the auto-solve feature you can use the `Basic_Sudoku.py` script which will solve it in terminal.
If you wish to use the animated version then you can replace a board in the `boards.txt` file to include your custom board, ensuring it is in the same format.
