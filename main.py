import sys
import numpy as np
from dokusan import generators
from solve import solve_board

""" This sudoku solver will take two types of command-line-arguments.
generate: Program will generate a sudoku board of varying difficulty from scratch, putting the data into a new .txt file and display the board.
    solve: Program will solve the existing sudoku board using a backtracking algorithm, and display the solved board.
    current: Program will display the current saved board
    """


def main():
    # Exit if no or too many commands given
    if len(sys.argv) != 2:
        sys.exit("Usage: main.py [command]")
    command = sys.argv[1].lower()
    if command == "generate":
        print("Enter difficulty: ", end="")
        while True:
            mode = input().lower()
            if mode == "easy" or mode == "normal" or mode == "hard":
                # Print a newly generated sudoku board
                print_board(generate_board(mode))
                break
            else:
                print("Easy, normal, or hard? ", end="")
    # Print the new board
    elif command == "solve" or "current":
        # Try to access the sudoku board unless it does not exist, then prompt user to generate a board
        try:
            with open("board.txt", "r") as file:
                sudoku = file.read()
                # Read text file into sudoku 9x9 grid, converting strs to ints
                board = [
                    list(map(int, lst)) for lst in np.array(list(sudoku)).reshape(9, 9)
                ]
        except FileNotFoundError:
            sys.exit("Found no board to solve. Try generating a new board first.")
        if command == "solve":
            solve_board(board)
        print_board(board)

    else:
        sys.exit("Invalid command. Enter 'generate', 'solve' or 'current'.")


# Generate a random sudoku board using dokusan generators library
def generate_board(mode):
    # Convert difficulty to rank to match required input
    match mode:
        case "easy":
            rank = 50
        case "normal":
            rank = 100
        case "hard":
            rank = 200
    with open("board.txt", "w") as file:
        # Write into file str of numbers that make up a valid sudoku board
        sudoku = str(generators.random_sudoku(avg_rank=rank))
        file.write(sudoku)

    # Return str of numbers into a a 9x9 list that is more readable
    new_board = np.array(list(sudoku)).reshape(9, 9)
    return new_board


# Printing the sudoku board in a readable and playable table
def print_board(board):
    # Loop through the whole board
    for i in range(9):
        if i % 3 == 0:
            # Separate each row block
            print(" -------------------------")

        # Loop through each row of the board plus 1 for end border
        for j in range(9):
            if int(board[i][j]) == 0:
                board[i][j] = " "
            # Separate each column block, to make 3x3 sections
            if j % 3 == 0:
                if j != 0:
                    print("| ", end="")
                else:
                    print(" | ", end="")
            if j == 8:
                print(str(board[i][j]) + " | ")
            else:
                print(str(board[i][j]) + " ", end="")
    print(" -------------------------")


if __name__ == "__main__":
    main()
