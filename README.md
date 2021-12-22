# Sudoku Game with Auto-solve - Ethan Hy
#### Video Demo:  <URL HERE>
#### Description:
This pygame app is a Sudoku game where you can play Sudoku normally and auto-solve it using the Magic button.
There is a timer and you have 3 lives, once you go below 0 lives you lose and must restart.

To play, click on an empty box and type in a number to sketch it in red. To submit a number, press enter whilst the box is selected.
If the number is incorrect you lose a life. 

If all the boxes are filled in then you have solved the Sudoku.

To restart the game press R on your keyboard.

On initial launch, the game starts off with an "Easy" difficulty board. You can change the difficulty by clicking on the arrows to navigate between Easy, Normal and Hard difficulties.

When the Magic button is clicked, the Sudoku is solved using a back tracking algorithm and animates each number submission.
If you wish to see this algorithm more clearly, you can introduce a delay between animated submissions in the code by uncommenting the following in `Sudoku.py`: `# pygame.time.delay(AUTO_DELAY)` within the `auto_solve` function.
Note that this will not change the .exe file and you will need to use an interpreter to run `Sudoku.py` or use pyinstaller with the command `pyinstaller --onefile Sudoku.py` to recreate the Sudoku.exe file.

If you wish to use the auto-solve feature you can use the `Basic_Sudoku.py` script which will solve it in terminal.
If you wish to use the animated version then you can replace a board in the `boards.txt` file to include your custom board, ensuring it is in the same format.