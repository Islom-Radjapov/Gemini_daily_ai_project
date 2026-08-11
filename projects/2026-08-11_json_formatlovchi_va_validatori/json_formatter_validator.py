"""
json_formatter_validator.py

A command-line utility for formatting and validating JSON data.
It supports pretty-printing, compact output, sorting keys, and reading/writing
from/to files or standard input/output. This utility uses only Python's
standard library.
"""

import json
import argparse
import sys
import os

__version__ = "1.0.0"

def _read_input_json(input_source):
    """
    Reads JSON data from the specified input source.

    Args:
        input_source (str or None): Path to the input file, or None/'-' for stdin.

    Returns:
        str: The raw JSON string read from the source.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: For other issues during file reading.
    """
    if input_source is None or input_source == '-':
        # Read from standard input
        try:
            return sys.stdin.read()
        except Exception as e:
            raise IOError(f"Error reading from stdin: {e}")
    else:
        # Read from a file
        try:
            with open(input_source, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Input file not found: '{input_source}'")
        except Exception as e:
            raise IOError(f"Error reading file '{input_source}': {e}")

def _write_output_json(output_data, output_destination):
    """
    Writes formatted JSON data to the specified output destination.

    Args:
        output_data (str): The formatted JSON string to write.
        output_destination (str or None): Path to the output file, or None for stdout.

    Raises:
        IOError: For issues during file writing.
    """
    if output_destination is None:
        # Write to standard output
        try:
            sys.stdout.write(output_data)
            if not output_data.endswith('\n'):
                sys.stdout.write('\n') # Ensure newline at the end
        except Exception as e:
            raise IOError(f"Error writing to stdout: {e}")
    else:
        # Write to a file
        try:
            with open(output_destination, 'w', encoding='utf-8') as f:
                f.write(output_data)
                if not output_data.endswith('\n'):
                    f.write('\n') # Ensure newline at the end
        except Exception as e:
            raise IOError(f"Error writing to file '{output_destination}': {e}")

def main():
    """
    Main function to parse arguments, format, and validate JSON data.
    """
    parser = argparse.ArgumentParser(
        description="A command-line utility to format and validate JSON data.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""Examples:
  # Format JSON from a file and print to console (default indent=2)
  python json_formatter_validator.py my_data.json

  # Format JSON from stdin and print to console with 4 spaces indent
  cat my_data.json | python json_formatter_validator.py -i 4

  # Format JSON from a file, sort keys, and save to another file
  python json_formatter_validator.py input.json -s -o output.json

  # Output JSON in a compact (single-line) format
  python json_formatter_validator.py input.json -c

  # Only validate JSON from a file, don't output anything if valid
  python json_formatter_validator.py input.json -v
"""
    )

    parser.add_argument(
        'input_source',
        nargs='?', # 0 or 1 argument
        default=None,
        help="Path to the input JSON file. If omitted or '-', reads from stdin."
    )
    parser.add_argument(
        '-o', '--output',
        metavar='FILE',
        help="Path to the output file. If omitted, writes to stdout."
    )
    parser.add_argument(
        '-i', '--indent',
        type=int,
        default=2,
        help="Number of spaces to use for indentation when pretty-printing. "
             "Default is 2. Use 0 for no indentation (single line) but still readable."
    )
    parser.add_argument(
        '-c', '--compact',
        action='store_true',
        help="Output JSON in a compact format (no indentation, no newlines). "
             "This overrides the --indent option."
    )
    parser.add_argument(
        '-s', '--sort-keys',
        action='store_true',
        help="Sort dictionary keys in the output JSON alphabetically."
    )
    parser.add_argument(
        '-v', '--validate-only',
        action='store_true',
        help="Only validate the JSON. If valid, print success message; "
             "otherwise, print error. No formatted output is produced."
    )
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}',
        help="Show program's version number and exit."
    )

    args = parser.parse_args()

    try:
        raw_json_string = _read_input_json(args.input_source)
    except (FileNotFoundError, IOError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

    if not raw_json_string.strip():
        print("Error: Input JSON is empty.", file=sys.stderr)
        sys.exit(1)

    try:
        # Attempt to parse (and thus validate) the JSON string
        json_data = json.loads(raw_json_string)

        if args.validate_only:
            print("JSON is valid.")
            sys.exit(0)

        # Prepare for formatting
        if args.compact:
            # Compact output: no indentation, tight separators
            formatted_json = json.dumps(json_data, sort_keys=args.sort_keys, separators=(',', ':'))
        else:
            # Pretty-print or simply no indentation based on args.indent
            formatted_json = json.dumps(json_data, indent=args.indent, sort_keys=args.sort_keys)

        _write_output_json(formatted_json, args.output)

    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format. {e}", file=sys.stderr)
        print("Please check your JSON syntax.", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()