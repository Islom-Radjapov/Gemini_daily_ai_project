"""
main.py

This is the main entry point for the Simple CLI Encryption Program.
It handles user interaction, displays menus, gets input, and calls
the encryption/decryption functions from cipher_utils.
"""

import sys  # Standard library module for system-specific parameters and functions
from cipher_utils import encrypt_caesar, decrypt_caesar

def display_menu():
    """Displays the main menu options to the user."""
    print("\n" + "="*40)
    print("  Simple CLI Encryption Program")
    print("="*40)
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Exit")
    print("="*40)

def get_user_choice() -> str:
    """
    Prompts the user for a menu choice and validates the input.

    Returns:
        str: The validated choice (e.g., '1', '2', '3').
    """
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
            print("-" * 40)

def get_message_input(prompt: str) -> str:
    """
    Prompts the user for a message and returns it.

    Args:
        prompt (str): The message to display to the user before input.

    Returns:
        str: The message entered by the user.
    """
    return input(prompt).strip()

def get_shift_input() -> int:
    """
    Prompts the user for a shift key and validates it as an integer.
    Continues to prompt until a valid integer is entered.

    Returns:
        int: The validated integer shift key.
    """
    while True:
        try:
            shift_str = input("Enter the shift key (an integer): ").strip()
            shift = int(shift_str)
            return shift
        except ValueError:
            print("Invalid input. Please enter an integer for the shift key.")
            print("-" * 40)

def main():
    """
    Main function to run the encryption program.
    It manages the program loop, user interactions, and calls
    the appropriate cipher functions.
    """
    while True:
        display_menu()
        choice = get_user_choice()
        print("-" * 40) # Separator for better readability

        if choice == '1':
            message = get_message_input("Enter the message to encrypt: ")
            shift = get_shift_input()
            encrypted_message = encrypt_caesar(message, shift)
            print("\n" + "="*40)
            print("  ENCRYPTION RESULT")
            print("="*40)
            print(f"Original Message:  {message}")
            print(f"Shift Key:         {shift}")
            print(f"Encrypted Message: {encrypted_message}")
            print("="*40)
        elif choice == '2':
            message = get_message_input("Enter the message to decrypt: ")
            shift = get_shift_input()
            decrypted_message = decrypt_caesar(message, shift)
            print("\n" + "="*40)
            print("  DECRYPTION RESULT")
            print("="*40)
            print(f"Encrypted Message: {message}")
            print(f"Shift Key:         {shift}")
            print(f"Decrypted Message: {decrypted_message}")
            print("="*40)
        elif choice == '3':
            print("\nExiting the program. Goodbye!")
            sys.exit(0) # Exit the program cleanly

        # Pause execution until the user presses Enter, for better user experience
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()