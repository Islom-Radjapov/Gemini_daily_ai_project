import random
import sys

# Define ANSI escape codes for text formatting
# These codes allow printing colored and styled text in the terminal.
# They are typically supported by most modern terminals.
ANSI_RESET = "\033[0m"
ANSI_BOLD = "\033[1m"
ANSI_BLUE = "\033[94m"
ANSI_GREEN = "\033[92m"
ANSI_YELLOW = "\033[93m"
ANSI_CYAN = "\033[96m"
ANSI_RED = "\033[91m"

# A list of quotes, each represented as a dictionary with 'quote' and 'author'.
# This serves as our simple database of quotes.
QUOTES = [
    {"quote": "The only way to do great work is to love what you do.", "author": "Steve Jobs"},
    {"quote": "Innovation distinguishes between a leader and a follower.", "author": "Steve Jobs"},
    {"quote": "Strive not to be a success, but rather to be of value.", "author": "Albert Einstein"},
    {"quote": "The mind is everything. What you think you become.", "author": "Buddha"},
    {"quote": "Eighty percent of success is showing up.", "author": "Woody Allen"},
    {"quote": "Your time is limited, don't waste it living someone else's life.", "author": "Steve Jobs"},
    {"quote": "The future belongs to those who believe in the beauty of their dreams.", "author": "Eleanor Roosevelt"},
    {"quote": "Tell me and I forget. Teach me and I remember. Involve me and I learn.", "author": "Benjamin Franklin"},
    {"quote": "The best way to predict the future is to create it.", "author": "Peter Drucker"},
    {"quote": "Life is what happens when you're busy making other plans.", "author": "John Lennon"},
    {"quote": "The only impossible journey is the one you never begin.", "author": "Tony Robbins"},
    {"quote": "Believe you can and you're halfway there.", "author": "Theodore Roosevelt"},
    {"quote": "The greatest glory in living lies not in never falling, but in rising every time we fall.", "author": "Nelson Mandela"},
    {"quote": "It is during our darkest moments that we must focus to see the light.", "author": "Aristotle Onassis"},
    {"quote": "Do not wait for leaders; do it alone, person to person.", "author": "Mother Teresa"},
    {"quote": "The journey of a thousand miles begins with a single step.", "author": "Lao Tzu"},
    {"quote": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "author": "Winston Churchill"},
    {"quote": "The only true wisdom is in knowing you know nothing.", "author": "Socrates"},
    {"quote": "To be yourself in a world that is constantly trying to make you something else is the greatest accomplishment.", "author": "Ralph Waldo Emerson"},
    {"quote": "What we achieve inwardly will change outer reality.", "author": "Plutarch"},
]

def get_formatted_text(text, color="", bold=False):
    """
    Applies ANSI escape codes to format text with color and/or bold.
    Checks if the output stream is a TTY to avoid printing codes in non-terminal environments.

    Args:
        text (str): The text to format.
        color (str, optional): An ANSI color code (e.g., ANSI_BLUE). Defaults to "".
        bold (bool, optional): Whether to make the text bold. Defaults to False.

    Returns:
        str: The formatted text string with ANSI codes, or original text if not in TTY.
    """
    if sys.stdout.isatty():  # Check if running in a terminal
        styles = []
        if bold:
            styles.append(ANSI_BOLD)
        if color:
            styles.append(color)

        if styles:
            return "".join(styles) + text + ANSI_RESET
    return text

def get_random_quote():
    """
    Selects and returns a random quote from the global QUOTES list.

    Returns:
        dict: A dictionary containing 'quote' and 'author' keys for the selected quote.
    """
    return random.choice(QUOTES)

def display_quote(quote_data):
    """
    Formats and prints a given quote and its author to the console.

    Args:
        quote_data (dict): A dictionary with 'quote' and 'author' keys.
    """
    quote_text = get_formatted_text(f'"{quote_data["quote"]}"', color=ANSI_CYAN, bold=True)
    author_text = get_formatted_text(f"- {quote_data["author"]}", color=ANSI_YELLOW)

    print("\n" + "=" * 50)
    print(quote_text)
    print(author_text.rjust(50)) # Right-align author for better presentation
    print("=" * 50 + "\n")

def display_menu():
    """
    Prints the interactive menu options to the console.
    """
    print(get_formatted_text("Choose an option:", color=ANSI_BLUE, bold=True))
    print(get_formatted_text("  1. Get a new random quote", color=ANSI_GREEN))
    print(get_formatted_text("  2. Exit", color=ANSI_RED))
    print("-" * 30)

def main():
    """
    Main function to run the Random Quote Generator application.
    It displays a welcome message, then enters a loop for user interaction.
    """
    print(get_formatted_text("<<< Welcome to the Random Quote Generator! >>>", color=ANSI_BLUE, bold=True))
    
    while True:
        display_menu()
        choice = input(get_formatted_text("Enter your choice (1 or 2): ", color=ANSI_BLUE)).strip()

        if choice == '1':
            quote = get_random_quote()
            display_quote(quote)
        elif choice == '2':
            print(get_formatted_text("\nThank you for using the Random Quote Generator. Goodbye!", color=ANSI_YELLOW, bold=True))
            sys.exit(0) # Exit the program cleanly
        else:
            print(get_formatted_text("Invalid choice. Please enter '1' or '2'.", color=ANSI_RED, bold=True))

if __name__ == "__main__":
    main()