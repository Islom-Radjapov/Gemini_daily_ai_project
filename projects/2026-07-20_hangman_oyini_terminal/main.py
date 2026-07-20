"""
This module contains ASCII art for the Hangman game, including the game logo
and the different stages of the hangman figure.
"""

# ASCII art for the game logo
LOGO = """
 _   _                                         
| | | | __ _ _ __   __ _ _ __ ___   __ _ _ __  
| |_| |/ _` | '_ \\ / _` | '_ ` _ \\ / _` | '_ \\ 
|  _  | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\\__,_|_| |_|\\__, |_| |_| |_|\\__,_|_| |_|
                   |___/                       
"""

# List of strings, where each string represents a stage of the hangman figure.
# The index corresponds to the number of incorrect guesses (lives lost).
HANGMAN_STAGES = [
    """
  +---+
  |   |
      |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
      |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
  |   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
      |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 /    |
      |
=========
""",
    """
  +---+
  |   |
  O   |
 /|\\  |
 / \\  |
      |
=========
"""
]