"""
Tic Tac Toe - Two Player Console Game
Run with: python tic_tac_toe.py
"""

def print_board(board):
    print()
    for i in range(3):
        row = " | ".join(board[i*3:i*3+3])
        print(f" {row} ")
        if i < 2:
            print("---+---+---")
    print()


def check_winner(board, player):
    win_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
        (0, 4, 8), (2, 4, 6)              # diagonals
    ]
    return any(all(board[i] == player for i in combo) for combo in win_combinations)


def is_board_full(board):
    return all(cell != " " for cell in board)


def get_move(board, player):
    while True:
        move = input(f"Player {player}, enter a position (1-9): ").strip()
        if not move.isdigit() or not (1 <= int(move) <= 9):
            print("Invalid input. Please enter a number between 1 and 9.")
            continue
        index = int(move) - 1
        if board[index] != " ":
            print("‼️ That spot is already taken. Try again. ‼️")
            continue
        return index


def play_game():
    board = [" "] * 9
    current_player = "X"

    print("Welcome to Tic Tac Toe!")
    print("Positions are numbered 1-9, left to right, top to bottom.")
    print_board(["1", "2", "3", "4", "5", "6", "7", "8", "9"])

    while True:
        print_board(board)
        move = get_move(board, current_player)
        board[move] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"🎉 Player {current_player} wins!")
            break

        if is_board_full(board):
            print_board(board)
            print("It's a draw!")
            break

        current_player = "O" if current_player == "X" else "X"

    play_again = input("Play again? (y/n): ").strip().lower()
    if play_again == "y":
        play_game()
    else:
        print("Thanks for playing!")


if __name__ == "__main__":
    play_game()