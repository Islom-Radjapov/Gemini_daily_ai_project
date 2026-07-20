import random
import os
import sys
from hangman_art import LOGO, HANGMAN_STAGES
from words import WORD_LIST

# Define constants for the game
MAX_LIVES = len(HANGMAN_STAGES) - 1  # Number of stages in hangman art, 0-indexed

def clear_screen():
    """
    Clears the terminal screen.
    Works for both Windows ('cls') and Unix-like systems ('clear').
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def get_random_word():
    """
    Selects a random word from the WORD_LIST.
    The word is converted to lowercase.
    Returns:
        str: A randomly chosen word.
    """
    return random.choice(WORD_LIST).lower()

def display_game_state(display_word, lives_left, guessed_letters_set):
    """
    Displays the current state of the Hangman game.
    Includes the hangman ASCII art, the partially guessed word, and
    the letters that have already been guessed.

    Args:
        display_word (list): A list of characters representing the word
                             with unguessed letters as underscores.
        lives_left (int): The number of lives the player has remaining.
        guessed_letters_set (set): A set of letters that have already been guessed.
    """
    print(HANGMAN_STAGES[MAX_LIVES - lives_left])  # Display current hangman stage
    print(f"\nWord: {' '.join(display_word)}")
    print(f"Lives remaining: {lives_left}")
    print(f"Guessed letters: {', '.join(sorted(list(guessed_letters_set)))}")
    print("-" * 30)

def play_hangman():
    """
    Main function to run the Hangman game.
    Initializes game state, handles user input, updates game state,
    and checks for win/loss conditions.
    """
    clear_screen()
    print(LOGO)
    print("Welcome to Hangman!\n")

    chosen_word = get_random_word()
    word_length = len(chosen_word)
    
    # Initialize game variables
    display_word = ["_"] * word_length
    lives = MAX_LIVES
    guessed_letters = set()
    game_over = False

    while not game_over:
        clear_screen()
        display_game_state(display_word, lives, guessed_letters)

        guess = input("Guess a letter: ").lower()

        # Input validation
        if not guess.isalpha():
            print("Invalid input! Please enter a letter.")
            input("Press Enter to continue...")
            continue
        if len(guess) != 1:
            print("Invalid input! Please enter a single letter.")
            input("Press Enter to continue...")
            continue
        if guess in guessed_letters:
            print(f"You've already guessed '{guess}'. Try again.")
            input("Press Enter to continue...")
            continue

        guessed_letters.add(guess) # Add the valid guess to the set of guessed letters

        # Check if the guessed letter is in the chosen word
        if guess in chosen_word:
            for position in range(word_length):
                letter = chosen_word[position]
                if letter == guess:
                    display_word[position] = letter
            print(f"Good guess! '{guess}' is in the word.")
        else:
            lives -= 1
            print(f"Wrong guess! '{guess}' is not in the word. You lose a life.")
        
        input("Press Enter to continue...")

        # Check for win condition
        if "_" not in display_word:
            game_over = True
            clear_screen()
            display_game_state(display_word, lives, guessed_letters)
            print("\n" + "="*30)
            print("CONGRATULATIONS! You won!")
            print(f"The word was: {chosen_word.upper()}")
            print("="*30 + "\n")

        # Check for loss condition
        if lives == 0:
            game_over = True
            clear_screen()
            display_game_state(display_word, lives, guessed_letters)
            print("\n" + "="*30)
            print("GAME OVER! You ran out of lives.")
            print(f"The word was: {chosen_word.upper()}")
            print("="*30 + "\n")

def main():
    """
    The main entry point of the program.
    Allows the user to play multiple rounds of Hangman.
    """
    while True:
        play_hangman()
        play_again = input("Do you want to play again? (yes/no): ").lower()
        if play_again not in ["yes", "y"]:
            print("Thanks for playing! Goodbye.")
            sys.exit() # Exit the program gracefully

if __name__ == "__main__":
    main()