# filename: currency_data.py

"""
This module stores static currency data used by the converter.
Since external API calls are not allowed (standard libraries only),
these exchange rates are hardcoded.
"""

# Exchange rates relative to USD (United States Dollar).
# E.g., 1 EUR is 1.0869 USD, 1 GBP is 1.27 USD.
# These rates are static and do not update in real-time.
EXCHANGE_RATES = {
    "USD": 1.00,  # United States Dollar (Base Currency for rates)
    "EUR": 1.0869, # Euro
    "GBP": 1.27,  # British Pound Sterling
    "JPY": 0.0067, # Japanese Yen (1 JPY is approx 0.0067 USD)
    "CAD": 0.73,  # Canadian Dollar
    "AUD": 0.66,  # Australian Dollar
    "CHF": 1.12,  # Swiss Franc
    "CNY": 0.138, # Chinese Yuan
    "INR": 0.012, # Indian Rupee
    "BRL": 0.19,  # Brazilian Real
    "RUB": 0.011, # Russian Ruble
    "KRW": 0.00073, # South Korean Won
    "MXN": 0.055, # Mexican Peso
    "SGD": 0.74,  # Singapore Dollar
    "HKD": 0.128, # Hong Kong Dollar
    "NZD": 0.61,  # New Zealand Dollar
    "SEK": 0.096, # Swedish Krona
    "NOK": 0.095, # Norwegian Krone
    "DKK": 0.14,  # Danish Krone
    "PLN": 0.24,  # Polish Złoty
    "TRY": 0.031, # Turkish Lira
    "ZAR": 0.053, # South African Rand
    "AED": 0.27,  # United Arab Emirates Dirham
    "SAR": 0.27,  # Saudi Riyal
    "UZS": 0.000079 # Uzbekistan Sum (1 UZS is approx 0.000079 USD)
}

# Full names for currency codes for display purposes.
CURRENCY_NAMES = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "GBP": "British Pound Sterling",
    "JPY": "Japanese Yen",
    "CAD": "Canadian Dollar",
    "AUD": "Australian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "INR": "Indian Rupee",
    "BRL": "Brazilian Real",
    "RUB": "Russian Ruble",
    "KRW": "South Korean Won",
    "MXN": "Mexican Peso",
    "SGD": "Singapore Dollar",
    "HKD": "Hong Kong Dollar",
    "NZD": "New Zealand Dollar",
    "SEK": "Swedish Krona",
    "NOK": "Norwegian Krone",
    "DKK": "Danish Krone",
    "PLN": "Polish Złoty",
    "TRY": "Turkish Lira",
    "ZAR": "South African Rand",
    "AED": "United Arab Emirates Dirham",
    "SAR": "Saudi Riyal",
    "UZS": "Uzbekistan Sum"
}

def get_available_currencies():
    """
    Returns a sorted list of available currency codes.
    """
    return sorted(EXCHANGE_RATES.keys())

def get_currency_name(code):
    """
    Returns the full name for a given currency code.
    """
    return CURRENCY_NAMES.get(code, code) # Return code itself if name not found