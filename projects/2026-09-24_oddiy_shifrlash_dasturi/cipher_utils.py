"""
cipher_utils.py

This module contains the core logic for Caesar cipher encryption and decryption.
It provides functions to shift individual characters and entire strings.
"""

ALPHABET_SIZE = 26  # Number of letters in the English alphabet (a-z)

def _shift_char(char: str, shift: int) -> str:
    """
    Helper function to shift a single alphabetic character.
    Handles both uppercase and lowercase letters, wrapping around the alphabet.
    Non-alphabetic characters are returned unchanged.

    Args:
        char (str): The character to be shifted.
        shift (int): The integer shift value.

    Returns:
        str: The shifted character, or the original character if not alphabetic.
    """
    if 'a' <= char <= 'z':
        start_ord = ord('a')
        # Apply shift, wrap around using modulo, then convert back to char
        shifted_ord = (ord(char) - start_ord + shift) % ALPHABET_SIZE + start_ord
        return chr(shifted_ord)
    elif 'A' <= char <= 'Z':
        start_ord = ord('A')
        shifted_ord = (ord(char) - start_ord + shift) % ALPHABET_SIZE + start_ord
        return chr(shifted_ord)
    else:
        # If not an alphabet character, return as is
        return char

def encrypt_caesar(text: str, shift: int) -> str:
    """
    Encrypts the given text using the Caesar cipher.
    Only alphabetic characters are shifted. Non-alphabetic characters
    (numbers, spaces, punctuation) remain unchanged.
    The shift value determines how many positions each letter is moved.

    Args:
        text (str): The plain text message to be encrypted.
        shift (int): The integer shift key to use for encryption.

    Returns:
        str: The encrypted text.
    """
    encrypted_text_chars = [_shift_char(char, shift) for char in text]
    return "".join(encrypted_text_chars)

def decrypt_caesar(text: str, shift: int) -> str:
    """
    Decrypts the given text using the Caesar cipher.
    This is essentially the same as encryption but with a negative shift.

    Args:
        text (str): The encrypted text message to be decrypted.
        shift (int): The integer shift key that was used for encryption.

    Returns:
        str: The decrypted text.
    """
    # Decryption is simply encryption with a negative shift (or ALPHABET_SIZE - shift)
    decrypted_text_chars = [_shift_char(char, -shift) for char in text]
    return "".join(decrypted_text_chars)