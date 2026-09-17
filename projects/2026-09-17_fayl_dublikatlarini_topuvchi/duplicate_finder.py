import os
import hashlib
import sys
from collections import defaultdict

def calculate_file_hash(filepath, hash_algorithm='md5', block_size=65536):
    """
    Calculates the hash of a file's content.

    Args:
        filepath (str): The path to the file.
        hash_algorithm (str): The hashing algorithm to use (e.g., 'md5', 'sha256').
                              Defaults to 'md5'.
        block_size (int): The size of chunks to read from the file.
                          Larger blocks improve performance for large files but use more memory.

    Returns:
        str: The hexadecimal digest of the file's hash, or None if an error occurs.
    """
    try:
        if hash_algorithm == 'md5':
            hasher = hashlib.md5()
        elif hash_algorithm == 'sha256':
            hasher = hashlib.sha256()
        else:
            print(f"Error: Unsupported hash algorithm '{hash_algorithm}'. Using 'md5'.", file=sys.stderr)
            hasher = hashlib.md5()

        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(block_size), b''):
                hasher.update(chunk)
        return hasher.hexdigest()
    except FileNotFoundError:
        print(f"Warning: File not found: {filepath}", file=sys.stderr)
        return None
    except PermissionError:
        print(f"Warning: Permission denied to read file: {filepath}", file=sys.stderr)
        return None
    except IOError as e:
        print(f"Warning: I/O error reading file {filepath}: {e}", file=sys.stderr)
        return None

def find_duplicate_files(directory_path):
    """
    Finds duplicate files within a given directory and its subdirectories.
    Duplicates are identified based on their content hash.

    Args:
        directory_path (str): The root directory to start scanning.

    Returns:
        dict: A dictionary where keys are file hashes and values are lists of
              full paths to files that share that hash (i.e., duplicates).
              Only groups with more than one file are included.
    """
    if not os.path.isdir(directory_path):
        print(f"Error: Directory not found or not a valid directory: {directory_path}", file=sys.stderr)
        return {}

    # defaultdict makes it easy to append to a list for a key that might not exist yet
    hashes_to_filepaths = defaultdict(list)
    processed_count = 0
    skipped_count = 0

    print(f"Scanning directory: {directory_path}")
    print("This might take a while for large directories...")

    for root, _, files in os.walk(directory_path):
        for filename in files:
            filepath = os.path.join(root, filename)
            if os.path.islink(filepath):
                # Skip symbolic links to avoid duplicate processing or infinite loops
                skipped_count += 1
                continue
            
            file_hash = calculate_file_hash(filepath)
            if file_hash:
                hashes_to_filepaths[file_hash].append(filepath)
                processed_count += 1
            else:
                skipped_count += 1 # File failed to hash
            
            # Optional: Print progress for large scans
            # if processed_count % 100 == 0:
            #     sys.stdout.write(f"\rProcessed {processed_count} files...")
            #     sys.stdout.flush()

    sys.stdout.write(f"\rFinished scanning {processed_count} files. Skipped {skipped_count} files due to errors/links.\n")
    sys.stdout.flush()

    duplicate_groups = {
        file_hash: filepaths
        for file_hash, filepaths in hashes_to_filepaths.items()
        if len(filepaths) > 1
    }

    return duplicate_groups

def main():
    """
    Main function to parse arguments and run the duplicate file finder.
    """
    if len(sys.argv) < 2:
        print("Usage: python duplicate_finder.py <directory_path>")
        print("Example: python duplicate_finder.py /home/user/documents")
        print("Example: python duplicate_finder.py . (to scan current directory)")
        sys.exit(1)

    target_directory = sys.argv[1]

    print("-" * 50)
    print(f"Starting Duplicate File Finder for: '{target_directory}'")
    print("-" * 50)

    duplicate_files = find_duplicate_files(target_directory)

    if not duplicate_files:
        print("\nNo duplicate files found in the specified directory.")
        print("-" * 50)
        return

    print("\n" + "=" * 50)
    print("Duplicate Files Found:")
    print("=" * 50)

    total_duplicate_files_count = 0
    duplicate_group_count = 0

    for file_hash, filepaths in duplicate_files.items():
        duplicate_group_count += 1
        print(f"\n--- Group {duplicate_group_count} (Hash: {file_hash[:10]}...) ---")
        print(f"  Found {len(filepaths)} files with identical content:")
        for path in filepaths:
            total_duplicate_files_count += 1
            print(f"    - {path}")
        print("-" * 15) # Small separator for readability between groups

    print("\n" + "=" * 50)
    print(f"Summary: Found {duplicate_group_count} groups of duplicate files.")
    print(f"Total duplicate files (including originals): {total_duplicate_files_count}")
    print("Please review the list above and consider deleting unwanted duplicates.")
    print("=" * 50)

if __name__ == "__main__":
    main()