import argparse
import sys
from markdown_parser import MarkdownParser

class MarkdownToHtmlConverter:
    """
    Manages the overall conversion process from Markdown to HTML.
    Includes an HTML template with inline styling for a modern look.
    """
    def __init__(self):
        self._parser = MarkdownParser()
        # Basic HTML template for the output, including inline CSS for professional design
        self._html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Markdown Conversion</title>
    <style>
        /* General Body Styling */
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol";
            line-height: 1.6;
            margin: 0 auto;
            max-width: 800px;
            padding: 20px;
            color: #333;
            background-color: #fcfcfc; /* Light background */
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); /* Subtle shadow for content area */
            border-radius: 8px; /* Rounded corners for the main content area */
            padding-top: 30px;
            padding-bottom: 30px;
        }}

        /* Headings */
        h1, h2, h3, h4, h5, h6 {{
            color: #222;
            margin-top: 1.5em; /* More spacing above headings */
            margin-bottom: 0.8em;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{ font-size: 2.8em; border-bottom: 2px solid #eee; padding-bottom: 0.5em; color: #1a1a1a; }}
        h2 {{ font-size: 2.2em; border-bottom: 1px solid #eee; padding-bottom: 0.4em; }}
        h3 {{ font-size: 1.7em; }}
        h4 {{ font-size: 1.4em; }}
        h5 {{ font-size: 1.1em; }}
        h6 {{ font-size: 0.9em; color: #555; text-transform: uppercase; }}

        /* Paragraphs */
        p {{
            margin-top: 1em;
            margin-bottom: 1em;
        }}

        /* Links */
        a {{
            color: #007bff; /* Primary blue for links */
            text-decoration: none;
            transition: color 0.2s ease-in-out;
        }}
        a:hover {{
            color: #0056b3;
            text-decoration: underline;
        }}

        /* Lists */
        ul, ol {{
            padding-left: 25px;
            margin-top: 1em;
            margin-bottom: 1em;
        }}
        li {{
            margin-bottom: 0.5em;
        }}

        /* Text Formatting */
        strong, b {{
            font-weight: 700;
            color: #1a1a1a; /* Stronger color for bold text */
        }}
        em, i {{
            font-style: italic;
            color: #555;
        }}

        /* Inline Code */
        code {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            background-color: #e9ecef; /* Lighter background for inline code */
            padding: 0.2em 0.5em;
            margin: 0;
            font-size: 88%;
            border-radius: 4px;
            color: #c43232; /* Reddish for code */
        }}

        /* Code Blocks */
        pre {{
            background-color: #282c34; /* Darker background for code blocks */
            color: #abb2bf; /* Light text for code */
            border-radius: 6px;
            padding: 1.2em;
            overflow-x: auto;
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 90%;
            line-height: 1.5;
            margin-top: 1.5em;
            margin-bottom: 1.5em;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
            margin: 0;
            border-radius: 0;
            font-size: 100%;
            color: inherit;
        }}

        /* Blockquotes */
        blockquote {{
            margin: 0;
            padding: 0.5em 1.5em;
            color: #6a737d;
            border-left: 0.3em solid #aed6f1; /* Light blue border */
            background-color: #e8f4fb; /* Very light blue background */
            border-radius: 5px;
            margin-top: 1.5em;
            margin-bottom: 1.5em;
        }}

        /* Horizontal Rule */
        hr {{
            height: 2px;
            padding: 0;
            margin: 30px 0;
            background-color: #e1e4e8;
            border: 0;
            border-radius: 1px;
        }}
    </style>
</head>
<body>
    {content}
</body>
</html>"""

    def convert(self, markdown_content: str) -> str:
        """
        Converts the raw Markdown content to a full HTML document.
        """
        html_body_content = self._parser.parse(markdown_content)
        return self._html_template.format(content=html_body_content)

def main():
    """
    Main function for the Markdown to HTML converter CLI.
    Handles command-line arguments and orchestrates the conversion process.
    """
    parser = argparse.ArgumentParser(
        description="A simple command-line tool to convert Markdown files to HTML, "
                    "using only standard Python libraries. Supports a basic subset of Markdown."
    )
    parser.add_argument(
        "-i", "--input",
        type=str,
        required=True,
        help="Path to the input Markdown file."
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        required=False,
        help="Path to the output HTML file. If not provided, output will be printed to stdout."
    )

    args = parser.parse_args()

    # Input file handling
    try:
        with open(args.input, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error reading input file '{args.input}': {e}", file=sys.stderr)
        sys.exit(1)

    # Perform conversion
    converter = MarkdownToHtmlConverter()
    html_output = converter.convert(markdown_content)

    # Output file handling or print to stdout
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(html_output)
            print(f"Successfully converted '{args.input}' to '{args.output}'.")
        except IOError as e:
            print(f"Error writing to output file '{args.output}': {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Print to standard output if no output file specified
        print(html_output)

if __name__ == "__main__":
    main()