import sys
from url_shortener_core import URLShortener

def display_help():
    """
    Displays the help message for the URL Shortener utility,
    detailing available commands and their usage.
    """
    print("---------------------------------------------")
    print("     Python URL Shortener Utility v1.0       ")
    print("---------------------------------------------")
    print("Usage:")
    print("  python main.py shorten <LONG_URL>")
    print("      Shortens the given LONG_URL and prints the generated short URL.")
    print("      Example: python main.py shorten https://www.example.com/very/long/path/to/page")
    print("\n  python main.py retrieve <SHORT_CODE_OR_URL>")
    print("      Retrieves the original long URL for the given SHORT_CODE or short URL.")
    print("      Example: python main.py retrieve abcdef")
    print("      Example: python main.py retrieve http://localhost:8000/abcdef")
    print("\n  python main.py list")
    print("      Lists all stored short URL mappings.")
    print("\n  python main.py delete <SHORT_CODE_OR_URL>")
    print("      Deletes the mapping for the given SHORT_CODE or short URL.")
    print("      Example: python main.py delete abcdef")
    print("      Example: python main.py delete http://localhost:8000/abcdef")
    print("\n  python main.py help")
    print("      Displays this help message.")
    print("---------------------------------------------")

def main():
    """
    Main function to parse command-line arguments and execute URL shortener operations.
    It initializes the URLShortener and calls the appropriate method based on user input.
    """
    # Initialize the URLShortener with a data file and a base URL.
    # The base_url simulates the domain for the shortened URLs.
    shortener = URLShortener(data_file='urls.json', base_url='http://localhost:8000/')

    if len(sys.argv) < 2:
        # If no arguments are provided, display help and exit.
        display_help()
        sys.exit(1)

    command = sys.argv[1].lower() # Get the command (e.g., 'shorten', 'retrieve')

    if command == 'shorten':
        if len(sys.argv) < 3:
            print("Error: Please provide a URL to shorten.")
            display_help()
            sys.exit(1)
        long_url = sys.argv[2]
        short_url = shortener.shorten_url(long_url)
        if short_url:
            print(f"Success: Shortened URL -> {short_url}")
    elif command == 'retrieve':
        if len(sys.argv) < 3:
            print("Error: Please provide a short code or short URL to retrieve.")
            display_help()
            sys.exit(1)
        short_code_or_url = sys.argv[2]
        long_url = shortener.get_long_url(short_code_or_url)
        if long_url:
            print(f"Success: Original URL for '{short_code_or_url}' -> {long_url}")
        else:
            print(f"Error: Short code or URL '{short_code_or_url}' not found in our database.")
    elif command == 'list':
        mappings = shortener.list_all_mappings()
        if mappings:
            print("\nAll Stored URL Mappings:")
            print("------------------------------------------------------------------------------------")
            for short_code, long_url in mappings.items():
                print(f"{shortener.base_url}{short_code} -> {long_url}")
            print("------------------------------------------------------------------------------------")
        else:
            print("Info: No URL mappings found in the database.")
    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Error: Please provide a short code or short URL to delete.")
            display_help()
            sys.exit(1)
        short_code_or_url = sys.argv[2]
        if shortener.delete_short_url(short_code_or_url):
            print(f"Success: Mapping for '{short_code_or_url}' has been deleted.")
        else:
            print(f"Error: Short code or URL '{short_code_or_url}' not found for deletion.")
    elif command == 'help':
        display_help()
    else:
        print(f"Error: Unknown command '{command}'.")
        display_help()
        sys.exit(1)

if __name__ == "__main__":
    main()