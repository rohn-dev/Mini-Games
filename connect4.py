"""
Connect 4 - Two Player Console Game
Players take turns dropping pieces into columns.
First to connect 4 in a row (horizontally, vertically, or diagonally) wins.
"""

ROWS = 6
COLS = 7

EMPTY = "."
PLAYER_PIECES = {1: "X", 2: "O"}


def create_board():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


def print_board(board):
    print()
    for row in board:
        print(" ".join(row))
    print(" ".join(str(c) for c in range(COLS)))
    print()


def is_valid_column(board, col):
    return 0 <= col < COLS and board[0][col] == EMPTY


def get_next_open_row(board, col):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            return row
    return None


def drop_piece(board, row, col, piece):
    board[row][col] = piece


def check_win(board, piece):
    # Horizontal
    for row in range(ROWS):
        for col in range(COLS - 3):
            if all(board[row][col + i] == piece for i in range(4)):
                return True

    # Vertical
    for row in range(ROWS - 3):
        for col in range(COLS):
            if all(board[row + i][col] == piece for i in range(4)):
                return True

    # Positive diagonal (down-right)
    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            if all(board[row + i][col + i] == piece for i in range(4)):
                return True

    # Negative diagonal (up-right)
    for row in range(3, ROWS):
        for col in range(COLS - 3):
            if all(board[row - i][col + i] == piece for i in range(4)):
                return True

    return False


def is_board_full(board):
    return all(board[0][col] != EMPTY for col in range(COLS))


def get_column_input(player):
    while True:
        raw = input(f"Player {player} ({PLAYER_PIECES[player]}), choose a column (0-{COLS - 1}): ")
        if raw.lower() in ("q", "quit", "exit"):
            return None
        if not raw.isdigit():
            print("Please enter a valid number.")
            continue
        col = int(raw)
        if col < 0 or col >= COLS:
            print(f"Column must be between 0 and {COLS - 1}.")
            continue
        return col


def play_game():
    board = create_board()
    current_player = 1
    game_over = False

    print("Welcome to Connect 4!")
    print("Player 1 is X, Player 2 is O.")
    print("Type 'q' at any time to quit.")
    print_board(board)

    while not game_over:
        col = get_column_input(current_player)

        if col is None:
            print("Thanks for playing!")
            return

        if not is_valid_column(board, col):
            print("That column is full or invalid. Try again.")
            continue

        row = get_next_open_row(board, col)
        piece = PLAYER_PIECES[current_player]
        drop_piece(board, row, col, piece)

        print_board(board)

        if check_win(board, piece):
            print(f"🎉 Player {current_player} ({piece}) wins! 🎉")
            game_over = True
        elif is_board_full(board):
            print("It's a draw! The board is full.")
            game_over = True
        else:
            current_player = 2 if current_player == 1 else 1

    play_again = input("Play again? (y/n): ")
    if play_again.lower().startswith("y"):
        play_game()
    else:
        print("Thanks for playing!")


if __name__ == "__main__":
    play_game()