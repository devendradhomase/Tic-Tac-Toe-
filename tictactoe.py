# Tic-Tac-Toe Game
# Two Player Console Based Game

# Display the game board
def display_board(board):
    print("\n")
    print("     |     |")
    print(f"  {board[0]}  |  {board[1]}  |  {board[2]}")
    print("_____|_____|_____")
    print("     |     |")
    print(f"  {board[3]}  |  {board[4]}  |  {board[5]}")
    print("_____|_____|_____")
    print("     |     |")
    print(f"  {board[6]}  |  {board[7]}  |  {board[8]}")
    print("     |     |")
    print()

 

# Check whether a player has won
def check_winner(board, player):
    winning_combinations = [
        (0, 1, 2),  # First row
        (3, 4, 5),  # Second row
        (6, 7, 8),  # Third row
        (0, 3, 6),  # First column
        (1, 4, 7),  # Second column
        (2, 5, 8),  # Third column
        (0, 4, 8),  # Diagonal
        (2, 4, 6)   # Diagonal
    ]

    for combination in winning_combinations:
        if all(board[position] == player for position in combination):
            return True

    return False


# Check whether the board is full
def check_draw(board):
    return all(position in ["X", "O"] for position in board)


# Main game function
def play_game():

    # Initial board
    board = ["1", "2", "3",
             "4", "5", "6",
             "7", "8", "9"]

    current_player = "X"

    print("=" * 40)
    print("        TIC-TAC-TOE GAME")
    print("=" * 40)

    print("\nPlayer 1 : X")
    print("Player 2 : O")
    print("Select a position from 1 to 9.")

    while True:

        display_board(board)

        print(f"Player {current_player}'s turn")

        # Take input from user
        try:
            position = int(input("Enter position (1-9): "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            continue

        # Validate position
        if position < 1 or position > 9:
            print("Please enter a number between 1 and 9.")
            continue

        index = position - 1

        # Check whether position is already occupied
        if board[index] in ["X", "O"]:
            print("Position already occupied! Choose another position.")
            continue

        # Place player's symbol
        board[index] = current_player

        # Check winner
        if check_winner(board, current_player):
            display_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        # Check draw
        if check_draw(board):
            display_board(board)
            print("Game Draw!")
            break

        # Change player
        if current_player == "X":
            current_player = "O"
        else:
            current_player = "X"


# Program execution
play_game()