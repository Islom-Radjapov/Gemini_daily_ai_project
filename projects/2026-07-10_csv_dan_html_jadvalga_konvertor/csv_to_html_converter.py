import csv
import argparse
import sys
import os

def get_html_css():
    """
    Returns the CSS styles for the HTML table.
    This CSS is embedded directly into the HTML file, providing a clean and modern design.
    """
    return """
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 20px;
            background-color: #f4f7f6;
            color: #333;
            line-height: 1.6;
        }
        .table-container {
            overflow-x: auto; /* Ensures responsiveness for narrow screens */
            margin: 20px auto;
            max-width: 90%; /* Max width for table container */
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            border-radius: 10px;
            background-color: #fff;
            padding: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            margin: 0;
            min-width: 700px; /* Minimum width to ensure desktop readability */
        }
        th, td {
            padding: 14px 18px;
            border-bottom: 1px solid #e0e0e0;
            white-space: nowrap; /* Prevent content from wrapping in cells */
        }
        thead th {
            background-color: #007bff;
            color: #ffffff;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        tbody tr:nth-child(even) {
            background-color: #f8f8f8;
        }
        tbody tr:hover {
            background-color: #e9f5ff;
            transition: background-color 0.3s ease;
        }
        td {
            color: #555;
        }
        .header {
            color: #0056b3;
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 10px;
            border-bottom: 2px solid #007bff;
        }
        .header h1 {
            font-size: 2.2em;
            margin: 0;
            padding: 10px 0;
        }
        .empty-message {
            text-align: center;
            padding: 40px;
            color: #777;
            font-size: 1.1em;
        }
    </style>
    """

def generate_html_table(headers, data):
    """
    Generates an HTML table string from provided headers and data.

    Args:
        headers (list): A list of strings representing the table headers.
        data (list of lists): A list of lists, where each inner list represents a row of data.

    Returns:
        str: A string containing the HTML <table> element.
    """
    if not headers and not data:
        return "<p class='empty-message'>No data available to display in the table.</p>"

    html_table = "<table>\n"

    # Table header
    html_table += "    <thead>\n        <tr>\n"
    for header in headers:
        # Basic HTML entity escaping for headers to prevent XSS and ensure proper display
        escaped_header = header.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
        html_table += f"            <th>{escaped_header}</th>\n"
    html_table += "        </tr>\n    </thead>\n"

    # Table body
    html_table += "    <tbody>\n"
    for row in data:
        html_table += "        <tr>\n"
        for cell in row:
            # Basic HTML entity escaping for data cells
            escaped_cell = str(cell).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;').replace("'", '&#x27;')
            html_table += f"            <td>{escaped_cell}</td>\n"
        html_table += "        </tr>\n"
    html_table += "    </tbody>\n"

    html_table += "</table>"
    return html_table

def convert_csv_to_html(csv_filepath, output_filepath):
    """
    Converts a CSV file to an HTML table file.

    Args:
        csv_filepath (str): The path to the input CSV file.
        output_filepath (str): The path where the HTML output will be saved.

    Returns:
        bool: True if conversion is successful, False otherwise.
    """
    headers = []
    data = []

    if not os.path.exists(csv_filepath):
        print(f"Error: CSV file not found at '{csv_filepath}'", file=sys.stderr)
        return False

    try:
        with open(csv_filepath, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            try:
                headers = next(reader)  # First row is headers
            except StopIteration:
                # CSV file is empty, no headers or data
                print(f"Warning: CSV file '{csv_filepath}' is empty.", file=sys.stderr)
                headers = []
                data = []

            for row in reader:
                data.append(row)
    except FileNotFoundError:
        # This case should ideally be caught by os.path.exists, but kept for robustness.
        print(f"Error: CSV file not found: {csv_filepath}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"Error reading CSV file '{csv_filepath}': {e}", file=sys.stderr)
        return False

    # Determine titles based on input file name
    base_filename = os.path.basename(csv_filepath)
    clean_filename = os.path.splitext(base_filename)[0].replace('_', ' ').title()

    if not headers and not data:
        # Special handling for completely empty CSV files
        html_table_content = generate_html_table([], [])
        title_text = f"Empty Table from {clean_filename}"
        h1_title_text = f"No Data Found in '{base_filename}'"
    else:
        html_table_content = generate_html_table(headers, data)
        title_text = f"{clean_filename} Data Table"
        h1_title_text = f"Data from '{base_filename}'"

    full_html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title_text}</title>
    {get_html_css()}
</head>
<body>
    <div class="header">
        <h1>{h1_title_text}</h1>
    </div>
    <div class="table-container">
        {html_table_content}
    </div>
</body>
</html>
"""

    try:
        with open(output_filepath, mode='w', encoding='utf-8') as outfile:
            outfile.write(full_html_content)
        return True
    except Exception as e:
        print(f"Error writing HTML file '{output_filepath}': {e}", file=sys.stderr)
        return False

def main():
    """
    Main function to parse command-line arguments and initiate the CSV to HTML conversion.
    """
    parser = argparse.ArgumentParser(
        description="Convert a CSV file into a stylish, standalone HTML table.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        '--input', '-i',
        type=str,
        required=True,
        help="Path to the input CSV file.\nExample: --input data.csv"
    )
    parser.add_argument(
        '--output', '-o',
        type=str,
        required=True,
        help="Path to the output HTML file.\nExample: --output report.html"
    )

    args = parser.parse_args()

    print(f"Attempting to convert CSV: '{args.input}' to HTML: '{args.output}'...")
    if convert_csv_to_html(args.input, args.output):
        print(f"Conversion successful! HTML table saved to '{args.output}'")
        # Provide user a hint on how to open the file
        print(f"You can open '{args.output}' in any web browser to view the table.")
    else:
        print("Conversion failed. Please check the error messages above.", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()