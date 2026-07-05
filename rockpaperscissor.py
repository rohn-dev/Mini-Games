# to create a rock paper scissor game in python
import random
choices=["rock", "paper", "scissors"]
computer_choice=random.choice(choices)
print("Welcome to Rock, Paper, Scissors!")
user_choice=input("Enter your choice (rock, paper, scissors): ").lower()
print("You chose:", user_choice)
if user_choice not in choices:
    print("Invalid choice. Please choose rock, paper, or scissors.")
print("Computer chose:", computer_choice)


if user_choice == computer_choice:
    print("It's a tie!")
elif (user_choice == "rock" and computer_choice == "scissors") or(user_choice == "paper" and computer_choice == "rock") or (user_choice == "scissors" and computer_choice == "paper"):
    print("You win!")
else:
    print("Computer wins!")
round_number = 1
while True:
    play_again = input("Do you want to play again? (y/n): ").lower()
    if play_again == "y":
        round_number += 1
        print(f"\nRound {round_number}:")
        computer_choice = random.choice(choices)
        user_choice = input("Enter your choice (rock, paper, scissors): ").lower()
        print("You chose:", user_choice)
        if user_choice not in choices:
            print("Invalid choice. Please choose rock, paper, or scissors.")
            continue
        print("Computer chose:", computer_choice)

        if user_choice == computer_choice:
            print("It's a tie!")
        elif (user_choice == "rock" and computer_choice == "scissors") or (user_choice == "paper" and computer_choice == "rock") or (user_choice == "scissors" and computer_choice == "paper"):
            print("You win!")
        else:
            print("Computer wins!")
    elif play_again == "n":
        print("Thanks for playing! Goodbye!")
        break
    else:
        print("Invalid input. Please enter 'y' or 'n'.")