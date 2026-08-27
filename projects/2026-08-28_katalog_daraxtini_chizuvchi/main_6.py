import sys
import os
from dir_tree_generator import generate_directory_tree

def main():
    """
    Main function to parse command-line arguments and print the directory tree.
    """
    # Default path is the current directory
    target_path = '.'
    max_depth = None

    # Parse command-line arguments
    # sys.argv[0] is the script name itself
    args = sys.argv[1:] 
    
    i = 0
    while i < len(args):
        arg = args[i]
        if arg == '-d' or arg == '--depth':
            # Check if there's a next argument for depth value
            if i + 1 < len(args):
                try:
                    max_depth = int(args[i+1])
                    if max_depth < 0:
                        print("Error: Maximum depth cannot be negative.", file=sys.stderr)
                        sys.exit(1)
                    i += 1 # Consume the depth value
                except ValueError:
                    print(f"Error: Invalid depth value '{args[i+1]}'. Please provide an integer.", file=sys.stderr)
                    sys.exit(1)
            else:
                print("Error: --depth option requires a value.", file=sys.stderr)
                sys.exit(1)
        elif arg.startswith('-'):
            # Handle unknown options
            print(f"Error: Unknown option '{arg}'.", file=sys.stderr)
            print("Usage: python main.py [path] [-d <depth>]", file=sys.stderr)
            sys.exit(1)
        else:
            # Assume any non-option argument is the target path
            target_path = arg
        i += 1

    # Generate and print the directory tree
    tree = generate_directory_tree(target_path, max_depth)
    print(tree)

if __name__ == "__main__":
    main()