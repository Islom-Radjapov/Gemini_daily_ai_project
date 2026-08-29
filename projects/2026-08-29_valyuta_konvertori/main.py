# filename: main.py

import sys
from currency_data import EXCHANGE_RATES, CURRENCY_NAMES, get_available_currencies, get_currency_name

def display_welcome_message():
    """
    Displays a decorative welcome message for the currency converter.
    """
    print("=" * 60)
    print("        💰 SIMPLE CLI CURRENCY CONVERTER 💰")
    print("=" * 60)
    print("Welcome! Convert amounts between various currencies.")
    print("Please note: Exchange rates are static and not real-time.")
    print("-" * 60)

def display_available_currencies():
    """
    Displays the list of available currencies in a formatted way.
    """
    print("\n--- Available Currencies ---")
    currencies = get_available_currencies()
    # Display currencies in columns for better readability
    num_cols = 4
    col_width = max(len(code) + len(get_currency_name(code)) + 5 for code in currencies) // num_cols
    
    for i in range(0, len(currencies), num_cols):
        row_items = []
        for currency_code in currencies[i:i + num_cols]:
            row_items.append(f"{currency_code} ({get_currency_name(currency_code)})".ljust(col_width))
        print("".join(row_items))
    print("-" * 60)

def get_valid_amount():
    """
    Prompts the user for an amount and validates it to be a positive number.
    Returns the valid amount as a float.
    """
    while True:
        try:
            amount_str = input("Enter the amount you want to convert: ").strip()
            amount = float(amount_str)
            if amount <= 0:
                print("Error: Amount must be a positive number. Please try again.")
            else:
                return amount
        except ValueError:
            print("Error: Invalid amount. Please enter a numerical value (e.g., 100.50).")

def get_valid_currency(prompt_message, exclude_currency=None):
    """
    Prompts the user for a currency code and validates its existence.
    Optionally excludes a specific currency to prevent identical source/target.
    Returns the valid currency code (uppercased).
    """
    available_codes = get_available_currencies()
    while True:
        currency_code = input(prompt_message).strip().upper()
        if currency_code in available_codes:
            if exclude_currency and currency_code == exclude_currency:
                print(f"Error: Source and target currency cannot be the same. Please choose a different currency.")
            else:
                return currency_code
        else:
            print(f"Error: Invalid currency code '{currency_code}'. Please choose from the available list.")
            display_available_currencies()

def convert_currency(amount, from_currency, to_currency):
    """
    Converts an amount from one currency to another using the predefined exchange rates.
    
    Args:
        amount (float): The amount to convert.
        from_currency (str): The currency code of the initial amount.
        to_currency (str): The currency code of the target currency.
        
    Returns:
        float: The converted amount.
    """
    # Convert the amount from the source currency to the base currency (USD)
    amount_in_usd = amount * EXCHANGE_RATES[from_currency]
    
    # Convert the amount from the base currency (USD) to the target currency
    converted_amount = amount_in_usd / EXCHANGE_RATES[to_currency]
    
    return converted_amount

def main():
    """
    Main function to run the currency converter application.
    Manages the overall flow, user interaction, and conversion logic.
    """
    display_welcome_message()

    while True:
        display_available_currencies()

        amount_to_convert = get_valid_amount()
        
        source_currency = get_valid_currency("Enter the source currency code (e.g., USD, EUR): ")
        
        target_currency = get_valid_currency("Enter the target currency code (e.g., GBP, JPY): ", exclude_currency=source_currency)

        try:
            converted_value = convert_currency(amount_to_convert, source_currency, target_currency)
            
            print("\n" + "=" * 60)
            print("          ✨ Conversion Result ✨")
            print("-" * 60)
            print(f"  {amount_to_convert:,.2f} {source_currency} ({get_currency_name(source_currency)})")
            print(f"  is equal to")
            print(f"  {converted_value:,.2f} {target_currency} ({get_currency_name(target_currency)})")
            print("=" * 60)

        except KeyError as e:
            print(f"An internal error occurred: Currency code not found in rates ({e}).")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        while True:
            another_conversion = input("\nDo you want to perform another conversion? (yes/no): ").strip().lower()
            if another_conversion in ["yes", "y"]:
                print("-" * 60)
                break # Exit inner loop, continue main loop
            elif another_conversion in ["no", "n"]:
                print("\nThank you for using the Simple CLI Currency Converter! Goodbye! 👋")
                sys.exit(0) # Exit the program
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()