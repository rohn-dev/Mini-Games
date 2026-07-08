
"""Simple CLI Blackjack game.

Run the file and follow prompts to play against the dealer.
"""
import random
import sys

SUITS = ("Hearts", "Diamonds", "Clubs", "Spades")
RANKS = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
VALUES = {r: int(r) for r in map(str, range(2, 11))}
VALUES.update({"J": 10, "Q": 10, "K": 10, "A": 11})


def create_deck():
    return [(rank, suit) for suit in SUITS for rank in RANKS]


def card_str(card):
    return f"{card[0]} of {card[1]}"


def hand_value(hand):
    total = sum(VALUES[card[0]] for card in hand)
    # Adjust for aces
    aces = sum(1 for card in hand if card[0] == "A")
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def deal_card(deck):
    return deck.pop()


def show_hands(player_hand, dealer_hand, hide_dealer_card=True):
    print("\nDealer:")
    if hide_dealer_card:
        print("  <hidden>")
        if len(dealer_hand) > 1:
            print(f"  {card_str(dealer_hand[1])}")
    else:
        for c in dealer_hand:
            print(f"  {card_str(c)}")
        print(f"  Value: {hand_value(dealer_hand)}")

    print("\nPlayer:")
    for c in player_hand:
        print(f"  {card_str(c)}")
    print(f"  Value: {hand_value(player_hand)}")


def player_turn(deck, player_hand):
    while True:
        if hand_value(player_hand) >= 21:
            break
        choice = input("Hit or Stand? (h/s): ").strip().lower()
        if choice in ("h", "hit"):
            player_hand.append(deal_card(deck))
            print(f"You drew: {card_str(player_hand[-1])}")
            if hand_value(player_hand) > 21:
                print("You busted!")
                break
        elif choice in ("s", "stand"):
            break
        else:
            print("Please enter 'h' to hit or 's' to stand.")


def dealer_turn(deck, dealer_hand):
    while hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))


def compare_hands(player_hand, dealer_hand):
    player_val = hand_value(player_hand)
    dealer_val = hand_value(dealer_hand)
    if player_val > 21:
        return "player_bust"
    if dealer_val > 21:
        return "dealer_bust"
    if player_val > dealer_val:
        return "player_win"
    if player_val < dealer_val:
        return "dealer_win"
    return "push"


def take_bet(chips):
    while True:
        bet = input(f"You have {chips} chips. Enter bet (or 'q' to quit): ").strip()
        if bet.lower() == "q":
            return None
        if not bet.isdigit():
            print("Enter a positive integer bet.")
            continue
        bet = int(bet)
        if bet <= 0:
            print("Bet must be greater than zero.")
            continue
        if bet > chips:
            print("You don't have enough chips.")
            continue
        return bet


def play_round(deck, chips):
    if len(deck) < 15:
        deck[:] = create_deck()
        random.shuffle(deck)
        print("Shuffling new deck...")

    bet = take_bet(chips)
    if bet is None:
        return chips, False

    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]

    print()
    show_hands(player_hand, dealer_hand, hide_dealer_card=True)

    # Check for immediate blackjack
    player_val = hand_value(player_hand)
    dealer_val = hand_value(dealer_hand)
    if player_val == 21 and dealer_val != 21:
        print("Blackjack! You win 1.5x your bet.")
        chips += int(bet * 1.5)
        return chips, True
    if dealer_val == 21 and player_val != 21:
        print("Dealer has Blackjack. You lose.")
        chips -= bet
        return chips, True

    # Player turn
    player_turn(deck, player_hand)

    # Dealer turn if player didn't bust
    if hand_value(player_hand) <= 21:
        dealer_turn(deck, dealer_hand)

    print()
    show_hands(player_hand, dealer_hand, hide_dealer_card=False)

    result = compare_hands(player_hand, dealer_hand)
    if result == "player_bust":
        print("You busted. You lose your bet.")
        chips -= bet
    elif result == "dealer_bust":
        print("Dealer busted. You win!")
        chips += bet
    elif result == "player_win":
        print("You win!")
        chips += bet
    elif result == "dealer_win":
        print("Dealer wins.")
        chips -= bet
    else:
        print("Push. Bet returned.")

    return chips, True


def main():
    print("Welcome to CLI Blackjack!")
    deck = create_deck()
    random.shuffle(deck)
    chips = 100

    while True:
        chips, played = play_round(deck, chips)
        if not played:
            print("Goodbye!")
            break
        if chips <= 0:
            print("You're out of chips. Game over.")
            break
        cont = input("Play another round? (y/n): ").strip().lower()
        if cont not in ("y", "yes"):
            print(f"You leave with {chips} chips. Thanks for playing!")
            break


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nExiting. Goodbye.")
        sys.exit(0)