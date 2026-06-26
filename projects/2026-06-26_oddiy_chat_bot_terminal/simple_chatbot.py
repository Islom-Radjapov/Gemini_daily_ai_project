import random
import time
import sys
import re

# --- Configuration ---
BOT_NAME = "SimpleBot"
RESPONSE_DELAY_SECONDS = 0.8

# --- Chatbot Knowledge Base ---
# A dictionary mapping patterns to a list of possible responses.
# Patterns will be checked in order.
KNOWLEDGE_BASE = {
    # Greetings
    r"hi|hello|hey": [
        "Hello there! How can I help you today?",
        "Hi! Nice to meet you.",
        "Hey! What's up?",
    ],
    # Questions about the bot
    r"how are you|how do you do": [
        "I'm just a program, but I'm functioning perfectly!",
        "I don't have feelings, but I'm ready to chat!",
        "As an AI, I'm always great!",
    ],
    r"who are you|what is your name": [
        f"I am {BOT_NAME}, your friendly terminal chatbot.",
        "You can call me Bot. I'm here to chat!",
        f"My name is {BOT_NAME}. What's yours?",
    ],
    r"what can you do|help": [
        "I can chat with you about various topics, or just keep you company. Try asking me something!",
        "I can answer some basic questions or just have a casual conversation. What's on your mind?",
    ],
    # Time/Date related (simple examples)
    r"what time is it": [
        "I don't have a real-time clock integration right now, but you can check your system's clock!",
        "Time flies when you're having fun, right?",
    ],
    r"tell me a joke": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "I told my wife she was drawing her eyebrows too high. She looked surprised.",
        "What do you call a fake noodle? An impasta!",
    ],
    # General positive/negative sentiment (very basic)
    r"good|great|awesome": [
        "That's great to hear!",
        "Glad you feel that way!",
    ],
    r"bad|sad|unhappy": [
        "I'm sorry to hear that. Is there anything I can do to cheer you up?",
        "I hope things get better soon.",
    ],
}

# --- Generic Fallback Responses ---
# Responses for when no specific pattern is matched.
GENERIC_RESPONSES = [
    "I'm not sure I understand. Can you rephrase that?",
    "That's an interesting thought! Tell me more.",
    "Hmm, I need more information to respond to that.",
    "Could you elaborate a bit?",
    "My apologies, I'm a simple bot and don't quite grasp that.",
]

# --- Exit Commands ---
EXIT_COMMANDS = ["bye", "exit", "quit", "goodbye"]

def display_message(sender, message):
    """
    Displays a message from either the bot or the user.
    Simulates typing delay for bot messages.
    """
    if sender == BOT_NAME:
        print(f"\n{sender}: ", end='', flush=True) # Print bot name and colon, wait for message
        for char in message:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.03) # Smaller delay for character by character display
        print() # New line after bot message
        time.sleep(RESPONSE_DELAY_SECONDS) # Overall delay before next input
    else:
        print(f"You: {message}")

def get_user_input():
    """
    Prompts the user for input and returns the trimmed, lowercase string.
    """
    return input("You: ").strip().lower()

def get_bot_response(user_input):
    """
    Determines the bot's response based on the user's input.
    """
    # Check for exit commands first
    if user_input in EXIT_COMMANDS:
        return "exit"

    # Iterate through the knowledge base to find a matching pattern
    for pattern, responses in KNOWLEDGE_BASE.items():
        if re.search(pattern, user_input):
            return random.choice(responses)

    # If no specific pattern matched, return a generic response
    return random.choice(GENERIC_RESPONSES)

def main():
    """
    Main function to run the chatbot.
    """
    display_message(BOT_NAME, f"Hello! I am {BOT_NAME}. How can I help you today? (Type 'bye' to exit)")

    while True:
        user_message = get_user_input()

        if not user_message: # Handle empty input
            display_message(BOT_NAME, "Please type something!")
            continue

        bot_response = get_bot_response(user_message)

        if bot_response == "exit":
            display_message(BOT_NAME, "It was nice chatting with you! Goodbye!")
            break
        else:
            display_message(BOT_NAME, bot_response)

if __name__ == "__main__":
    main()