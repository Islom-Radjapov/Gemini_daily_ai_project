import re
import sys

def display_section_header(title: str):
    """
    Prints a formatted section header for better readability in the CLI.

    Args:
        title (str): The title of the section.
    """
    print(f"\n{'=' * 60}")
    print(f"  {title.upper()}")
    print(f"{'=' * 60}")

def display_result(label: str, value):
    """
    Prints a labeled result in a consistent format.

    Args:
        label (str): The descriptive label for the result.
        value: The value to be displayed.
    """
    print(f"{label:<25}: {value}")

def run_regex_tester():
    """
    Main function to run the interactive regex tester application.
    It continuously prompts the user for regex patterns and text,
    then displays the results of re.search(), re.findall(), and re.sub().
    """
    print("=" * 60)
    print("        Welcome to the Python Regex Tester!         ")
    print("=" * 60)
    print("This utility helps you test regular expressions interactively.")
    print("Enter your regex pattern and text to see the results.")
    print("Type 'q' (or 'quit') at any prompt to exit the program.")

    while True:
        display_section_header("New Test Session")

        # Get regex pattern from user
        pattern_input = input("Enter regex pattern (e.g., r'\\d+') [q to quit]: ").strip()
        if pattern_input.lower() in ['q', 'quit']:
            break

        # Get text to test against from user
        text_input = input("Enter text to search in (e.g., 'Hello 123 World') [q to quit]: ").strip()
        if text_input.lower() in ['q', 'quit']:
            break

        print("\n" + "-" * 60)
        display_result("Pattern", pattern_input)
        display_result("Text", text_input)
        print("-" * 60)

        try:
            # Compile the regex pattern for efficiency and to catch syntax errors early
            compiled_pattern = re.compile(pattern_input)

            # --- Test re.search() ---
            display_section_header("re.search() - First Match Details")
            match = compiled_pattern.search(text_input)
            if match:
                display_result("Match Found", "YES")
                display_result("Full Match (Group 0)", match.group(0))
                for i, group in enumerate(match.groups(), 1):
                    display_result(f"Group {i}", group)
                display_result("Start Index", match.start())
                display_result("End Index", match.end())
            else:
                display_result("Match Found", "NO")
                print("No match was found for the given pattern in the text.")

            # --- Test re.findall() ---
            display_section_header("re.findall() - All Non-overlapping Matches")
            all_matches = compiled_pattern.findall(text_input)
            if all_matches:
                display_result("Total Matches", len(all_matches))
                for i, m in enumerate(all_matches):
                    display_result(f"Match {i+1}", f"'{m}'")
            else:
                display_result("Total Matches", "0")
                print("No non-overlapping matches found.")

            # --- Test re.sub() ---
            display_section_header("re.sub() - Substitution Operation")
            sub_replacement = input(
                "Enter replacement string for re.sub() (leave empty to skip): "
            ).strip()
            if sub_replacement:
                # Perform substitution and count replacements
                substituted_text, count = compiled_pattern.subn(sub_replacement, text_input)
                display_result("Original Text", text_input)
                display_result("Replacement String", sub_replacement)
                display_result("Substituted Text", substituted_text)
                display_result("Replacements Made", count)
            else:
                print("re.sub() operation skipped.")

        except re.error as e:
            # Handle invalid regex pattern errors
            print(f"\nERROR: Invalid regex pattern syntax: {e}")
            print("Please check your pattern and try again.")
        except Exception as e:
            # Catch any other unexpected errors
            print(f"\nAN UNEXPECTED ERROR OCCURRED: {e}")
            print("Please report this issue if it persists.")

        print("\n" + "=" * 60)
        print("          Test complete. Ready for a new test.          ")
        print("=" * 60 + "\n")

    print("\n" + "=" * 60)
    print("Thank you for using the Python Regex Tester. Goodbye!")
    print("=" * 60)
    sys.exit(0) # Exit cleanly

if __name__ == "__main__":
    run_regex_tester()