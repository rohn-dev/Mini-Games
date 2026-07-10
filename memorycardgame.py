import os
import random
import time


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def create_deck():
    symbols = ["A", "B", "C", "D", "E", "F", "G", "H"]
    deck = symbols + symbols
    random.seed(42)
    random.shuffle(deck)
    return deck


def display_board(cards, revealed):
    print("Memory Card Game")
    print("Match all pairs to win!")
    print()

    for row in range(0, len(cards), 4):
        board_row = cards[row:row + 4]
        revealed_row = revealed[row:row + 4]
        formatted = []

        for index, is_revealed in enumerate(revealed_row):
            position = row + index + 1
            if is_revealed:
                formatted.append(f"[{board_row[index]}]")
            else:
                formatted.append(f"[{position}]")

        print(" ".join(formatted))

    print()


def get_two_positions(card_count):
    while True:
        choice = input("Choose two card positions (1-{}), or type 'q' to quit: ".format(card_count)).strip().lower()
        if choice == "q" or choice == "quit":
            return None

        parts = choice.split()
        if len(parts) != 2:
            print("Please enter exactly two numbers.")
            continue

        try:
            pos1 = int(parts[0]) - 1
            pos2 = int(parts[1]) - 1
        except ValueError:
            print("Please enter valid numbers.")
            continue

        if not (0 <= pos1 < card_count and 0 <= pos2 < card_count):
            print("Positions must be between 1 and {}.".format(card_count))
            continue

        if pos1 == pos2:
            print("Choose two different cards.")
            continue

        return pos1, pos2


def play_game():
    cards = create_deck()
    revealed = [False] * len(cards)
    matched = [False] * len(cards)
    moves = 0

    while not all(matched):
        clear_screen()
        display_board(cards, revealed)
        print("Moves:", moves)

        choice = get_two_positions(len(cards))
        if choice is None:
            print("Thanks for playing!")
            return

        pos1, pos2 = choice

        if matched[pos1] or matched[pos2]:
            print("Those cards are already matched.")
            time.sleep(0.7)
            continue

        revealed[pos1] = True
        revealed[pos2] = True
        clear_screen()
        display_board(cards, revealed)

        if cards[pos1] == cards[pos2]:
            matched[pos1] = True
            matched[pos2] = True
            print("Nice! You found a match!")
            moves += 1
            time.sleep(1)
        else:
            print("No match. Try again!")
            moves += 1
            time.sleep(1.2)
            revealed[pos1] = False
            revealed[pos2] = False

    clear_screen()
    display_board(cards, revealed)
    print("Congratulations! You matched all the cards in {} moves!".format(moves))


if __name__ == "__main__":
    play_game()
