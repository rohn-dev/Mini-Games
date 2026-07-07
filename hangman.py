# hangman game
import random

# list of words to choose from
word_list = ["python", "java", "javascript", "hangman", "programming", "computer", "algorithm", "function", "variable", "loop"]

# choose a random word from the list
word = random.choice(word_list) 

lives = 6  # number of lives the player has
guessed_letters = []  # list to keep track of guessed letters
while True:
    # display the current state of the word
    display_word = ""
    for letter in word:
        if letter in guessed_letters:
            display_word += letter + " "
        else:
            display_word += "_ "
    print(display_word.strip())

    # check if the player has won
    if "_" not in display_word:
        print("Congratulations! You've guessed the word:", word)
        break

    # get the player's guess
    guess = input("Guess a letter: ").lower()

    # check if the guess is valid
    if len(guess) != 1 or not guess.isalpha():
        print("Please enter a single letter.")
        continue

    # check if the letter has already been guessed
    if guess in guessed_letters:
        print("You've already guessed that letter.")
        continue

    # add the guessed letter to the list
    guessed_letters.append(guess)

    # check if the guess is correct
    if guess in word:
        print("Good guess!")
    else:
        lives -= 1
        print(f"Wrong guess! You have {lives} lives left.")

    # check if the player has run out of lives
    if lives == 0:
        print("Game over! The word was:", word)
        break
