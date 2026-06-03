import json
from my_yaml_parser import parse_yaml, YamlParseError

def main():
    """
    Main function to demonstrate the YAML parser.
    It reads `example.yaml`, parses it, and prints the resulting
    Python object (dictionary or list).
    """
    yaml_file_path = 'example.yaml'

    try:
        # Read the content of the YAML file
        with open(yaml_file_path, 'r', encoding='utf-8') as f:
            yaml_content = f.read()

        print(f"--- Parsing YAML from '{yaml_file_path}' ---")
        # Parse the YAML content using our custom parser
        parsed_data = parse_yaml(yaml_content)
        
        print("\n--- Parsed Data (Python Object) ---")
        # Use json.dumps for pretty printing the resulting Python dictionary/list.
        # This makes the output readable and helps confirm the parsed structure.
        print(json.dumps(parsed_data, indent=2, ensure_ascii=False))

        print("\n--- Accessing specific data points ---")
        # Demonstrate how to access data from the parsed Python object
        if isinstance(parsed_data, dict):
            print(f"Project Name: {parsed_data.get('project_name', 'N/A')}")
            print(f"Project Version: {parsed_data.get('version', 'N/A')}")
            
            if 'settings' in parsed_data and isinstance(parsed_data['settings'], dict):
                print(f"Debug Mode: {parsed_data['settings'].get('debug_mode', 'N/A')} (Type: {type(parsed_data['settings'].get('debug_mode'))})")
                print(f"Log Level: {parsed_data['settings'].get('log_level', 'N/A')}")
                print(f"Empty Setting: {parsed_data['settings'].get('empty_setting', 'N/A')} (Type: {type(parsed_data['settings'].get('empty_setting'))})")
                print(f"Null Value: {parsed_data['settings'].get('null_value', 'N/A')} (Type: {type(parsed_data['settings'].get('null_value'))})")
                print(f"False Value: {parsed_data['settings'].get('false_value', 'N/A')} (Type: {type(parsed_data['settings'].get('false_value'))})")
                print(f"PI Value: {parsed_data['settings'].get('pi_value', 'N/A')} (Type: {type(parsed_data['settings'].get('pi_value'))})")

            if 'features' in parsed_data and isinstance(parsed_data['features'], list):
                print(f"Number of Features: {len(parsed_data['features'])}")
                if parsed_data['features']:
                    # Accessing an item in a list of dictionaries
                    first_feature = parsed_data['features'][0]
                    if isinstance(first_feature, dict):
                        print(f"First Feature Name: {first_feature.get('name', 'N/A')}")
                        print(f"First Feature Status: {first_feature.get('status', 'N/A')}")
            
            if 'description' in parsed_data:
                print(f"Description (first 50 chars): {parsed_data['description'][:50]}...")
                print(f"Description (last 50 chars): ...{parsed_data['description'][-50:]}")
        else:
            print("Root of YAML is a list. Cannot access 'project_name' directly.")

    except FileNotFoundError:
        print(f"Error: The file '{yaml_file_path}' was not found. Please ensure it is in the same directory as 'main.py'.")
    except YamlParseError as e:
        print(f"YAML Parsing Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()