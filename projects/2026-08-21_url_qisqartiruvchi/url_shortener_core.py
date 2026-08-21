import json
import os
import random
import string
from urllib.parse import urlparse

class URLShortener:
    """
    A simple URL shortener utility that stores mappings in a JSON file.
    It provides functionality to shorten long URLs, retrieve original URLs
    from short codes, list all mappings, and delete existing mappings.
    """
    def __init__(self, data_file='urls.json', base_url='http://localhost:8000/'):
        """
        Initializes the URLShortener with a data file and base URL.

        Args:
            data_file (str): The path to the JSON file for storing URL mappings.
            base_url (str): The base URL to prepend to generated short codes.
                            This simulates the domain where short URLs would be hosted.
        """
        self.data_file = data_file
        self.base_url = base_url if base_url.endswith('/') else f"{base_url}/"
        self.mappings = self._load_data()
        self.short_code_length = 6 # Default length for generated short codes

    def _load_data(self):
        """
        Loads URL mappings from the JSON data file.
        If the file does not exist or is empty/malformed, returns an empty dictionary.

        Returns:
            dict: A dictionary of short_code -> long_url mappings.
        """
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    # Handle cases where the file is empty or contains invalid JSON
                    print(f"Warning: '{self.data_file}' is empty or corrupted. Starting with an empty database.")
                    return {}
        return {}

    def _save_data(self):
        """
        Saves current URL mappings to the JSON data file.
        The data is saved with an indent for readability.
        """
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.mappings, f, indent=4, ensure_ascii=False)

    def _generate_short_code(self):
        """
        Generates a unique random alphanumeric short code.
        It continuously generates codes until a unique one (not already in mappings) is found.

        Returns:
            str: A unique short code.
        """
        # Characters allowed in short codes: uppercase letters, lowercase letters, and digits
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(self.short_code_length))
            if short_code not in self.mappings:
                return short_code

    def _is_valid_url(self, url):
        """
        Checks if a given string is a valid URL by parsing its components.
        A URL is considered valid if it has both a scheme (e.g., http, https)
        and a network location (e.g., example.com).

        Args:
            url (str): The URL string to validate.

        Returns:
            bool: True if the URL is valid, False otherwise.
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def shorten_url(self, long_url):
        """
        Shortens a given long URL and stores the mapping.
        If the URL is invalid, an error message is printed.
        If the URL has already been shortened, its existing short URL is returned.

        Args:
            long_url (str): The original long URL.

        Returns:
            str or None: The generated short URL if successful, None if the URL is invalid.
        """
        if not self._is_valid_url(long_url):
            print(f"Error: '{long_url}' is not a valid URL. Please provide a URL starting with http:// or https://")
            return None

        # Check if URL already exists in our mappings, return its short code if so
        for short_code, existing_long_url in self.mappings.items():
            if existing_long_url == long_url:
                print(f"Info: This URL has already been shortened to {self.base_url}{short_code}")
                return f"{self.base_url}{short_code}"

        # Generate a new unique short code
        short_code = self._generate_short_code()
        self.mappings[short_code] = long_url
        self._save_data() # Persist the new mapping
        return f"{self.base_url}{short_code}"

    def get_long_url(self, short_code_or_url):
        """
        Retrieves the original long URL for a given short code or a full short URL.
        It extracts the short code if a full URL is provided.

        Args:
            short_code_or_url (str): The short code or the full short URL.

        Returns:
            str or None: The original long URL if found, None otherwise.
        """
        # If a full short URL is provided, extract the short code part
        if short_code_or_url.startswith(self.base_url):
            short_code = short_code_or_url[len(self.base_url):]
        else:
            short_code = short_code_or_url

        return self.mappings.get(short_code)

    def list_all_mappings(self):
        """
        Returns all stored URL mappings.

        Returns:
            dict: A dictionary of all short_code -> long_url mappings.
        """
        return self.mappings

    def delete_short_url(self, short_code_or_url):
        """
        Deletes a short URL mapping.
        It extracts the short code if a full URL is provided.

        Args:
            short_code_or_url (str): The short code or the full short URL to delete.

        Returns:
            bool: True if the mapping was deleted, False if not found.
        """
        # Extract the short code if a full short URL is provided
        if short_code_or_url.startswith(self.base_url):
            short_code = short_code_or_url[len(self.base_url):]
        else:
            short_code = short_code_or_url

        if short_code in self.mappings:
            del self.mappings[short_code]
            self._save_data() # Persist the deletion
            return True
        return False