import os

def _generate_tree_recursive(path, prefix, level, max_depth):
    """
    Recursively generates the string representation of a directory tree.

    Args:
        path (str): The current directory path to traverse.
        prefix (str): The prefix string to add before each item to maintain tree structure.
        level (int): The current depth level of the traversal.
        max_depth (int | None): The maximum depth to traverse. None for no limit.

    Returns:
        str: A string segment representing the tree from the current path downwards.
    """
    if max_depth is not None and level > max_depth:
        return ""

    # Get all contents (files and directories) and sort them alphabetically
    try:
        contents = sorted(os.listdir(path))
    except PermissionError:
        return f"{prefix}└── [Permission Denied]\n"
    except Exception as e:
        return f"{prefix}└── [Error: {e}]\n"

    directories = [item for item in contents if os.path.isdir(os.path.join(path, item))]
    files = [item for item in contents if os.path.isfile(os.path.join(path, item))]

    # Combine directories and files for consistent iteration order
    all_items = directories + files
    num_items = len(all_items)

    output = ""
    for i, item in enumerate(all_items):
        is_last = (i == num_items - 1) # Check if this is the last item in the current directory
        
        # Choose the appropriate connector for the current item
        connector = "└── " if is_last else "├── "
        
        item_path = os.path.join(path, item)
        
        if os.path.isdir(item_path):
            # Append directory name with a trailing slash
            output += f"{prefix}{connector}{item}/\n"
            # Determine the prefix for children: '    ' if current item is last, '│   ' otherwise
            new_prefix_for_children = prefix + ("    " if is_last else "│   ")
            # Recursively call for subdirectories
            output += _generate_tree_recursive(item_path, new_prefix_for_children, level + 1, max_depth)
        else:
            # Append file name
            output += f"{prefix}{connector}{item}\n"
            
    return output

def generate_directory_tree(path='.', max_depth=None):
    """
    Generates a string representation of the directory tree starting from the given path.
    
    Args:
        path (str): The starting path. Defaults to the current directory ('.').
        max_depth (int | None): The maximum depth to traverse. None for no limit.

    Returns:
        str: A string representing the directory tree, or an error message if the path is invalid.
    """
    # Validate the input path
    if not os.path.exists(path):
        return f"Error: Path '{path}' does not exist."
    if not os.path.isdir(path):
        return f"Error: Path '{path}' is not a directory."

    # Get the base name of the starting directory for the root display
    # os.path.abspath resolves '.' to the full current directory name
    root_dir_name = os.path.basename(os.path.abspath(path))

    # Initialize the tree output with the root directory name
    tree_output = f"{root_dir_name}/\n"

    # Start the recursive generation from level 0 (children of the root)
    tree_output += _generate_tree_recursive(path, "", 0, max_depth)
    return tree_output