import os
import importlib.util
import sys
import inspect

# Import the core testing framework components
from micro_test import TestCase, TestRunner

def discover_test_files(directory="."):
    """
    Discovers Python files in the specified directory that start with 'test_'.
    These files are considered test modules.
    """
    test_files = []
    for entry in os.listdir(directory):
        if entry.startswith("test_") and entry.endswith(".py"):
            test_files.append(os.path.join(directory, entry))
    return sorted(test_files) # Sort for consistent discovery order

def load_tests_from_file(filepath):
    """
    Dynamically loads a Python module from a given file path
    and extracts all TestCase subclasses defined within it.
    """
    test_classes = []
    # Create a unique module name from the file path to avoid conflicts
    module_name = os.path.splitext(os.path.basename(filepath))[0] + "_" + \
                  str(hash(filepath))[:8].replace('-', '_')

    # Add the directory of the test file to sys.path temporarily
    # This allows test files to import other local modules if needed.
    original_sys_path = sys.path[:]
    test_file_dir = os.path.dirname(os.path.abspath(filepath))
    if test_file_dir not in sys.path:
        sys.path.insert(0, test_file_dir)

    try:
        # Create a module spec and load the module
        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec is None:
            print(f"Warning: Could not create module spec for {filepath}")
            return []
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module # Register the module
        spec.loader.exec_module(module) # Execute the module's code

        # Inspect the module for classes that inherit from TestCase
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, TestCase) and obj is not TestCase:
                test_classes.append(obj)
    except Exception as e:
        print(f"Error loading tests from {filepath}: {e}")
    finally:
        # Always restore original sys.path
        if test_file_dir in sys.path:
            sys.path.remove(test_file_dir)
        # sys.path = original_sys_path # A simpler way, but less precise if other path changes happened

    return test_classes

def main():
    """
    Main entry point for the PyMiniTest runner.
    It discovers test files, loads test classes, runs them, and reports results.
    """
    print("PyMiniTest - A Simple Python Unit Test Framework\n")

    current_directory = os.getcwd()
    test_files = discover_test_files(current_directory)

    if not test_files:
        print(f"No test files found in '{current_directory}' (looking for 'test_*.py').")
        sys.exit(0) # Exit successfully if no tests were found

    all_test_classes = []
    print("Discovering test classes:")
    for test_file in test_files:
        print(f"  Loading tests from {os.path.basename(test_file)}...")
        classes = load_tests_from_file(test_file)
        if classes:
            for cls in classes:
                print(f"    Found test class: {cls.__name__}")
            all_test_classes.extend(classes)
        else:
            print(f"    No TestCase classes found in {os.path.basename(test_file)}")
    
    if not all_test_classes:
        print("\nNo TestCase classes found to run after discovery.")
        sys.exit(0) # Exit successfully if no test classes were found

    print("\n" + "=" * 50)
    print("STARTING TEST EXECUTION")
    print("=" * 50)

    runner = TestRunner()
    results = runner.run(all_test_classes)

    # Exit with a non-zero status code if any tests failed or encountered errors.
    # This is standard practice for CI/CD pipelines.
    if results["failed"] > 0 or results["errors"] > 0:
        sys.exit(1) # Indicate failure
    else:
        sys.exit(0) # Indicate success

if __name__ == "__main__":
    main()