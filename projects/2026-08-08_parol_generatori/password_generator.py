import random
import string
import argparse
import sys

def generate_password(
    length,
    include_lowercase=True,
    include_uppercase=True,
    include_digits=True,
    include_special=True
):
    """
    Generates a random password based on specified criteria.

    Args:
        length (int): The desired length of the password.
        include_lowercase (bool): True to include lowercase letters, False otherwise.
        include_uppercase (bool): True to include uppercase letters, False otherwise.
        include_digits (bool): True to include digits, False otherwise.
        include_special (bool): True to include special characters, False otherwise.

    Returns:
        str: The generated password.

    Raises:
        ValueError: If no character types are selected or if the length is too small
                    to accommodate all required character types.
    """
    # Define character sets using the 'string' module
    lowercase_chars = string.ascii_lowercase
    uppercase_chars = string.ascii_uppercase
    digit_chars = string.digits
    special_chars = string.punctuation

    # List to hold all available characters for the password
    all_available_chars = []
    # List to hold at least one character from each selected type
    guaranteed_chars = []

    if include_lowercase:
        all_available_chars.extend(lowercase_chars)
        guaranteed_chars.append(random.choice(lowercase_chars))
    if include_uppercase:
        all_available_chars.extend(uppercase_chars)
        guaranteed_chars.append(random.choice(uppercase_chars))
    if include_digits:
        all_available_chars.extend(digit_chars)
        guaranteed_chars.append(random.choice(digit_chars))
    if include_special:
        all_available_chars.extend(special_chars)
        guaranteed_chars.append(random.choice(special_chars))

    # Check if any character types were selected
    if not all_available_chars:
        raise ValueError("At least one character type (lowercase, uppercase, digits, or special characters) must be selected.")

    # Check if the requested length is sufficient for guaranteed characters
    if length < len(guaranteed_chars):
        raise ValueError(
            f"Password length ({length}) is too short to include at least one of each selected character type ({len(guaranteed_chars)} required)."
        )

    # Fill the remaining length with random characters from all available characters
    for _ in range(length - len(guaranteed_chars)):
        guaranteed_chars.append(random.choice(all_available_chars))

    # Shuffle the list to randomize the position of guaranteed characters
    random.shuffle(guaranteed_chars)

    # Join the characters to form the final password string
    return "".join(guaranteed_chars)

def main():
    """
    Main function to parse arguments and generate the password.
    """
    parser = argparse.ArgumentParser(
        description="Generate a strong, random password with customizable options.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "-l", "--length",
        type=int,
        default=12,
        help="The desired length of the password (default: 12)."
    )
    parser.add_argument(
        "--include-lowercase",
        action="store_true",
        default=True,
        help="Include lowercase letters in the password (default: True)."
    )
    parser.add_argument(
        "--no-lowercase",
        action="store_false",
        dest="include_lowercase",
        help="Exclude lowercase letters from the password."
    )
    parser.add_argument(
        "--include-uppercase",
        action="store_true",
        default=True,
        help="Include uppercase letters in the password (default: True)."
    )
    parser.add_argument(
        "--no-uppercase",
        action="store_false",
        dest="include_uppercase",
        help="Exclude uppercase letters from the password."
    )
    parser.add_argument(
        "--include-digits",
        action="store_true",
        default=True,
        help="Include digits (0-9) in the password (default: True)."
    )
    parser.add_argument(
        "--no-digits",
        action="store_false",
        dest="include_digits",
        help="Exclude digits from the password."
    )
    parser.add_argument(
        "--include-special",
        action="store_true",
        default=True,
        help="Include special characters (e.g., !@#$) in the password (default: True)."
    )
    parser.add_argument(
        "--no-special",
        action="store_false",
        dest="include_special",
        help="Exclude special characters from the password."
    )

    args = parser.parse_args()

    # Validate password length
    if args.length <= 0:
        print("Error: Password length must be a positive integer.", file=sys.stderr)
        sys.exit(1)

    try:
        password = generate_password(
            args.length,
            args.include_lowercase,
            args.include_uppercase,
            args.include_digits,
            args.include_special
        )
        print(f"Generated Password: {password}")
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()