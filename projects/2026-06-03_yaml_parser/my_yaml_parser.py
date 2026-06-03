import re

class YamlParseError(Exception):
    """
    Custom exception for YAML parsing errors.
    """
    pass

def _get_indent(line):
    """
    Calculates the leading whitespace (indentation) of a line.
    """
    return len(line) - len(line.lstrip(' '))

def _strip_comment(line):
    """
    Removes comments from a line. A comment starts with '#' and goes to the end of the line.
    """
    comment_idx = line.find('#')
    if comment_idx != -1:
        return line[:comment_idx].rstrip()
    return line.rstrip()

def _coerce_value(value_str):
    """
    Converts a string value to its appropriate Python type (int, float, bool, None).
    Handles basic YAML scalar types.
    """
    value_str = value_str.strip()

    # If the string is empty after stripping, it represents a None value.
    if not value_str:
        return None

    # Booleans: YAML accepts 'true', 'True', 'yes', 'Yes', 'on', 'On' for True;
    # and 'false', 'False', 'no', 'No', 'off', 'Off' for False.
    if value_str.lower() in ('true', 'yes', 'on'):
        return True
    if value_str.lower() in ('false', 'no', 'off'):
        return False

    # Null values: YAML accepts 'null', 'Null', 'NULL', '~'.
    if value_str.lower() in ('null', '~'):
        return None

    # Numbers: Try converting to integer first, then to float.
    try:
        return int(value_str)
    except ValueError:
        pass
    try:
        return float(value_str)
    except ValueError:
        pass

    # Strings: If wrapped in single or double quotes, strip them.
    # This simplified parser does not handle complex escape sequences within quoted strings.
    if (value_str.startswith("'") and value_str.endswith("'")) or \
       (value_str.startswith('"') and value_str.endswith('"')):
        return value_str[1:-1]
    
    # If no other type matches, it's a string.
    return value_str

def parse_yaml(yaml_string):
    """
    Parses a simplified YAML string into a Python dictionary or list.
    This parser supports:
    - Key-value pairs (mappings)
    - Lists (sequences)
    - Nested mappings and sequences using indentation
    - Basic scalar types: strings, integers, floats, booleans, null
    - Comments (lines starting with # or comments after a value)
    - Literal block scalars (`|`)

    It uses only standard Python libraries and a single pass, stack-based approach
    to handle indentation.
    """
    lines_with_info = []
    # Pre-process lines to extract indentation, stripped content, and original line number for error reporting.
    for line_num, line in enumerate(yaml_string.splitlines()):
        stripped_line = _strip_comment(line)
        if stripped_line:
            lines_with_info.append((_get_indent(line), stripped_line, line_num + 1))

    if not lines_with_info:
        # If the YAML string is empty or contains only comments/empty lines, return an empty dictionary.
        return {}

    # Determine the type of the root object (dictionary or list) based on the first significant line.
    first_indent, first_line_content, _ = lines_with_info[0]
    if first_line_content.startswith('- '):
        root_object = []
    else:
        root_object = {}

    # The context stack stores tuples: (current_object, current_indent_level)
    # The initial entry represents the conceptual parent of the root object.
    # Its indent level is set to -1 to allow 0-indented root elements to be considered children.
    context_stack = [(root_object, -1)]

    idx = 0
    while idx < len(lines_with_info):
        current_indent, current_line_content, line_num = lines_with_info[idx]
        
        # Adjust the stack: pop contexts that are no longer in scope due to reduced indentation.
        # This loop ensures that `current_context_obj` always points to the correct parent for the current line.
        while len(context_stack) > 1 and current_indent <= context_stack[-1][1]:
            context_stack.pop()
        
        current_context_obj, current_context_indent = context_stack[-1]

        # Basic validation for indentation: current line should not be less indented than its parent.
        # This acts as a safeguard against malformed YAML after stack adjustments.
        if current_indent < current_context_indent:
            raise YamlParseError(f"Bad indentation at line {line_num}: '{current_line_content}'. "
                                 f"Indent {current_indent} is less than parent's {current_context_indent}.")
        
        # --- Process Mapping (key-value pair) ---
        match_mapping = re.match(r'([^:]+):\s*(.*)', current_line_content)
        if match_mapping:
            key = match_mapping.group(1).strip()
            value_str = match_mapping.group(2).strip()

            # A mapping item (key: value) must be added to a dictionary context.
            if not isinstance(current_context_obj, dict):
                raise YamlParseError(f"Cannot add mapping item '{key}' to a list context at line {line_num}.")

            if value_str == '|': # Literal block scalar indicator
                block_text_lines = []
                block_content_start_idx = idx + 1 # Start checking for block content from the next line
                
                # Iterate through subsequent lines to collect block content.
                block_current_idx = block_content_start_idx
                while block_current_idx < len(lines_with_info):
                    b_indent, b_content, _ = lines_with_info[block_current_idx]
                    # Block content lines must be strictly more indented than the 'key: |' line.
                    if b_indent > current_indent:
                        # For simplicity, this parser appends the already stripped content.
                        # A fully compliant YAML parser would strip a common minimal indent from the *original* lines
                        # to precisely preserve relative indentation within the block.
                        block_text_lines.append(b_content)
                        block_current_idx += 1
                    else:
                        break # Block ends when indentation is less than or equal to the key's indent
                
                current_context_obj[key] = '\n'.join(block_text_lines)
                idx = block_current_idx # Advance the main index past the block content
                continue # Skip `idx += 1` at the end of the loop, as `idx` is already updated

            elif not value_str: # Key with no value, expecting a nested block or `None`
                next_line_idx = idx + 1
                # Check if the next line is more indented, indicating a nested structure.
                if next_line_idx < len(lines_with_info) and lines_with_info[next_line_idx][0] > current_indent:
                    next_indent, next_content, _ = lines_with_info[next_line_idx]
                    if next_content.startswith('- '): # Nested list block
                        new_list = []
                        current_context_obj[key] = new_list
                        context_stack.append((new_list, next_indent)) # Push new list onto stack as the current context
                    else: # Nested dictionary block
                        new_dict = {}
                        current_context_obj[key] = new_dict
                        context_stack.append((new_dict, next_indent)) # Push new dict onto stack as the current context
                else:
                    current_context_obj[key] = None # Key with an explicit `None` value (empty)
            else: # Simple key-value pair on the same line
                current_context_obj[key] = _coerce_value(value_str)

        # --- Process Sequence (list item) ---
        elif re.match(r'- (\s*)(.*)', current_line_content):
            match_sequence = re.match(r'- (\s*)(.*)', current_line_content)
            value_str_after_dash = match_sequence.group(2).strip()

            # A sequence item (`- item`) must be added to a list context.
            if not isinstance(current_context_obj, list):
                raise YamlParseError(f"Cannot add sequence item to a dictionary context at line {line_num}.")

            next_line_idx = idx + 1
            # Check if this list item is empty (`- `) and followed by an indented block (nested dict or list).
            if not value_str_after_dash and \
               next_line_idx < len(lines_with_info) and lines_with_info[next_line_idx][0] > current_indent:
                next_indent, next_content, _ = lines_with_info[next_line_idx]
                if next_content.startswith('- '): # Nested list item (e.g., `- \n  - sub_item`)
                    new_list_item = []
                    current_context_obj.append(new_list_item)
                    context_stack.append((new_list_item, next_indent)) # Push new list onto stack
                else: # Nested dictionary item (e.g., `- \n  key: value`)
                    new_dict_item = {}
                    current_context_obj.append(new_dict_item)
                    context_stack.append((new_dict_item, next_indent)) # Push new dict onto stack
            elif value_str_after_dash:
                # List item has a value on the same line. Could be a scalar or an inline mapping.
                match_inline_mapping = re.match(r'([^:]+):\s*(.*)', value_str_after_dash)
                if match_inline_mapping: # e.g., `- name: Alice` (short-hand map in a list)
                    inline_key = match_inline_mapping.group(1).strip()
                    inline_value = match_inline_mapping.group(2).strip()
                    new_dict_item = {inline_key: _coerce_value(inline_value)}
                    current_context_obj.append(new_dict_item)
                    
                    # If this inline mapping is followed by more indented lines (e.g., `- name: Alice\n  id: 101`),
                    # those lines belong to this `new_dict_item`. So, push it onto the stack as the current context.
                    if next_line_idx < len(lines_with_info) and lines_with_info[next_line_idx][0] > current_indent:
                        next_indent, _, _ = lines_with_info[next_line_idx]
                        context_stack.append((new_dict_item, next_indent)) # Push this new dict as the current context
                else: # Simple scalar value, e.g., `- item_value`
                    current_context_obj.append(_coerce_value(value_str_after_dash))
            else: # An empty list item (just `-` with no value or nested block)
                current_context_obj.append(None)
        else:
            raise YamlParseError(f"Invalid YAML syntax or unexpected content at line {line_num}: '{current_line_content}'.")

        idx += 1 # Move to the next line for processing

    return root_object