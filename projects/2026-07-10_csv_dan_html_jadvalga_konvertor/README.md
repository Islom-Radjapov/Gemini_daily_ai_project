# CSV to HTML Table Converter

## Project Description
This Python utility script provides a robust and elegant solution for transforming raw CSV (Comma Separated Values) data into a beautifully formatted, standalone HTML table. It's designed as a quick visualization tool, enabling users to convert tabular data into a web-friendly format that can be easily viewed in any browser, shared, or embedded. The resulting HTML file is self-contained, with all styling (CSS) embedded directly, ensuring no external dependencies.

## Features
*   **Standard CSV Support:** Reads and correctly parses standard CSV files, automatically identifying the first row as table headers.
*   **Stylish & Modern Design:** Generates an HTML table with a clean, professional, and visually appealing design using inline CSS. Features include distinct headers, hover effects, and zebra-striping for improved readability.
*   **Responsive Layout:** The generated HTML table includes basic responsiveness, ensuring it adapts reasonably well to different screen sizes, especially on larger displays.
*   **Standalone Output:** Produces a single HTML file that encapsulates both the data and its complete styling, eliminating the need for separate CSS files or internet access to render correctly.
*   **Command-Line Interface (CLI):** User-friendly command-line arguments facilitate easy specification of input CSV and output HTML file paths.
*   **Robust Error Handling:** Includes checks for file existence and handles potential issues during file reading or writing, providing clear error messages.
*   **HTML Escaping:** Automatically escapes special characters in CSV data when converting to HTML, preventing potential cross-site scripting (XSS) vulnerabilities and ensuring data is displayed correctly.

## How to Run
This project requires Python 3.x. It utilizes only Python's standard library, meaning no `pip install` commands are necessary.

1.  **Save the script:** Download or copy the `csv_to_html_converter.py` script to a directory on your computer.
2.  **Prepare a CSV file:** Ensure you have a CSV file ready that you wish to convert. An `example_input.csv` is provided within this project for demonstration purposes.
3.  **Execute from the command line:** Open your terminal or command prompt, navigate to the directory where you saved the script, and run the following command: