import sys
import argparse

# Constants for QR-like code generation
GRID_SIZE = 31  # Default grid size (similar to QR Version 1, but simplified)
DEFAULT_BLACK_CHAR = '█' # Unicode full block character
DEFAULT_WHITE_CHAR = ' ' # Space character

def text_to_bit_stream(text):
    """
    Converts a string into a list of binary bits (0s and 1s).
    Each character is represented by 8 bits (its ASCII value).
    """
    bit_stream = []
    for char in text:
        # Get ASCII value, convert to binary, remove '0b' prefix, pad with leading zeros to 8 bits
        binary_char = bin(ord(char))[2:].zfill(8)
        for bit in binary_char:
            bit_stream.append(int(bit))
    return bit_stream

def create_empty_grid(size):
    """
    Initializes an empty square grid with None values.
    """
    return [[None for _ in range(size)] for _ in range(size)]

def place_finder_pattern(grid, start_row, start_col):
    """
    Places a 7x7 finder pattern at the specified top-left corner.
    A finder pattern is a 7x7 square with a 1x1 black border,
    a 1x1 white inner border, and a 3x3 black square in the center.
    '1' represents a black module, '0' represents a white module.
    """
    pattern = [
        [1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1],
    ]
    for r in range(7):
        for c in range(7):
            # Place the pattern modules directly.
            # In this simplified design, finder patterns are placed first and
            # their positions are fixed, so no need to check for existing values.
            grid[start_row + r][start_col + c] = pattern[r][c]

def place_timing_patterns(grid):
    """
    Places horizontal and vertical timing patterns.
    These are alternating black/white modules that help a scanner
    determine the module density. They run along row 6 and column 6,
    between the finder patterns.
    """
    grid_size = len(grid)
    
    # Horizontal timing pattern (along row 6)
    # It runs from column 7 (after the top-left finder) to grid_size - 7 (before the top-right finder).
    for c in range(7, grid_size - 7):
        # Only fill if the cell is currently empty (None), as finder patterns are already placed.
        # This prevents overwriting parts of the finder patterns if their layout were different.
        if grid[6][c] is None:
            grid[6][c] = 1 if (c % 2 == 0) else 0 # Alternating black (1) and white (0)

    # Vertical timing pattern (along column 6)
    # It runs from row 7 (after the top-left finder) to grid_size - 7 (before the bottom-left finder).
    for r in range(7, grid_size - 7):
        # Only fill if the cell is currently empty (None).
        if grid[r][6] is None:
            grid[r][6] = 1 if (r % 2 == 0) else 0 # Alternating black (1) and white (0)

def fill_data_area(grid, bit_stream):
    """
    Fills the remaining empty cells in the grid with the bit stream.
    Data is filled row by row, skipping cells already occupied by patterns.
    If the bit stream runs out, remaining cells are filled with alternating 0s and 1s
    to prevent large blank areas and maintain a visual pattern.
    """
    grid_size = len(grid)
    bit_index = 0
    alternating_fill = 0 # Start with 0 for alternating fill pattern

    for r in range(grid_size):
        for c in range(grid_size):
            if grid[r][c] is None: # Only fill cells that are currently empty
                if bit_index < len(bit_stream):
                    grid[r][c] = bit_stream[bit_index]
                    bit_index += 1
                else:
                    # If the bit stream is exhausted, fill remaining cells with alternating pattern
                    grid[r][c] = alternating_fill
                    alternating_fill = 1 - alternating_fill # Toggle between 0 and 1

    # Check if there are any remaining bits that could not fit into the grid
    if bit_index < len(bit_stream):
        sys.stderr.write(f"Warning: Input text is too long for the {grid_size}x{grid_size} grid. "
                         f"Only {bit_index // 8} out of {len(bit_stream) // 8} characters were encoded.\n")

def render_ascii_qr(grid, black_char=DEFAULT_BLACK_CHAR, white_char=DEFAULT_WHITE_CHAR):
    """
    Converts the grid (containing 0s and 1s) into an ASCII string
    using the specified black and white characters.
    """
    output_lines = []
    for row in grid:
        line = ""
        for cell in row:
            if cell == 1: # Black module
                line += black_char
            else: # White module (cell == 0)
                line += white_char
        output_lines.append(line)
    return "\n".join(output_lines)

def generate_ascii_qr_code(text, grid_size=GRID_SIZE, black_char=DEFAULT_BLACK_CHAR, white_char=DEFAULT_WHITE_CHAR):
    """
    Orchestrates the generation of a QR-like ASCII matrix code.
    1. Converts text to a bit stream.
    2. Initializes an empty grid.
    3. Places fixed finder and timing patterns.
    4. Fills the remaining areas with data bits.
    5. Renders the final grid as an ASCII string.
    """
    if not isinstance(text, str) or not text:
        raise ValueError("Input text must be a non-empty string.")

    bit_stream = text_to_bit_stream(text)
    
    grid = create_empty_grid(grid_size)

    # Place the three primary finder patterns
    place_finder_pattern(grid, 0, 0) # Top-left corner
    place_finder_pattern(grid, 0, grid_size - 7) # Top-right corner
    place_finder_pattern(grid, grid_size - 7, 0) # Bottom-left corner

    # Place timing patterns
    place_timing_patterns(grid)

    # Fill the data area with the encoded bit stream
    fill_data_area(grid, bit_stream)

    # Render the final grid into an ASCII string using specified characters
    return render_ascii_qr(grid, black_char, white_char)

def main():
    """
    Main function to parse command-line arguments and generate the ASCII QR-like code.
    """
    parser = argparse.ArgumentParser(
        description="Generates a simple QR-like ASCII matrix code from input text. "
                    "Note: This is a simplified ASCII matrix code generator using only "
                    "standard Python libraries, not a full QR code standard implementation."
    )
    parser.add_argument(
        "text",
        nargs="?", # Makes the text argument optional, allowing pipe input
        help="The text to encode into the ASCII QR-like code. If not provided, input will be read from stdin."
    )
    parser.add_argument(
        "-o", "--output",
        help="Output file path (e.g., 'qr_code.txt'). If not specified, the code will be printed to the console."
    )
    parser.add_argument(
        "-s", "--size",
        type=int,
        default=GRID_SIZE,
        help=f"Grid size (e.g., 31 for {GRID_SIZE}x{GRID_SIZE}). Must be an odd number and at least 21. Default: {GRID_SIZE}."
    )
    parser.add_argument(
        "-b", "--black",
        default=DEFAULT_BLACK_CHAR,
        help=f"Character for black modules. Default: '{DEFAULT_BLACK_CHAR}' (Unicode full block)."
    )
    parser.add_argument(
        "-w", "--white",
        default=DEFAULT_WHITE_CHAR,
        help=f"Character for white modules. Default: '{DEFAULT_WHITE_CHAR}' (space)."
    )

    args = parser.parse_args()

    input_text = args.text
    if not input_text:
        # If no text provided as a command-line argument, try reading from stdin
        if not sys.stdin.isatty(): # Check if stdin is being piped to
            input_text = sys.stdin.read().strip()
        else:
            # If no text argument and not piped, print help and exit
            parser.print_help()
            sys.exit("Error: No input text provided. Use 'python ascii_qr_generator.py \"Your Text\"' or pipe text (e.g., 'echo \"Hello\" | python ascii_qr_generator.py').")
            
    if not input_text: # After potentially reading from stdin, check if it's still empty
        sys.exit("Error: Input text is empty.")

    # Validate grid size argument
    if args.size < 21 or args.size % 2 == 0:
        sys.exit("Error: Grid size must be an odd number and at least 21 to accommodate patterns.")
    
    try:
        # Generate the ASCII QR-like code with specified parameters
        qr_ascii = generate_ascii_qr_code(
            input_text, 
            grid_size=args.size, 
            black_char=args.black, 
            white_char=args.white
        )

        if args.output:
            # Save the generated code to a file
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(qr_ascii)
                print(f"ASCII QR-like code saved to '{args.output}'")
            except IOError as e:
                sys.stderr.write(f"Error saving to file '{args.output}': {e}\n")
                sys.exit(1)
        else:
            # Print the generated code to the console
            print(qr_ascii)

    except ValueError as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)
    except Exception as e:
        sys.stderr.write(f"An unexpected error occurred: {e}\n")
        sys.exit(1)

if __name__ == "__main__":
    main()