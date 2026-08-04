import argparse
import sys
import os
from log_analyzer import LogAnalyzer # Assuming log_analyzer.py is in the same directory

def print_statistics(stats, filtered_levels=None):
    """
    Prints the gathered statistics in a user-friendly format.
    """
    print("\n" + "="*50)
    print(" " * 15 + "LOG FILE STATISTICS")
    print("="*50)

    print(f"Total lines in file: {stats['total_lines']}")
    print(f"Successfully parsed lines: {stats['parsed_lines']}")
    print("\n--- Log Level Distribution ---")
    
    # Sort levels for consistent output, with critical levels first
    sorted_levels = sorted(stats['level_counts'].items(), key=lambda item: (
        0 if item[0] == 'CRITICAL' else
        1 if item[0] == 'ERROR' else
        2 if item[0] == 'WARNING' else
        3 if item[0] == 'INFO' else
        4 if item[0] == 'DEBUG' else 5
    ))

    total_filtered_level_count = sum(count for _, count in sorted_levels)
    if filtered_levels:
        print(f"(Showing counts for levels: {', '.join(filtered_levels)})")
    
    if sorted_levels:
        for level, count in sorted_levels:
            print(f"  [{level}]: {count}")
    else:
        print("  No log entries found for the specified levels.")
    
    print(f"Total entries counted for specified levels: {total_filtered_level_count}")

    print("\n--- Time Range ---")
    if stats['first_timestamp'] and stats['last_timestamp']:
        print(f"First log entry: {stats['first_timestamp'].strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}")
        print(f"Last log entry:  {stats['last_timestamp'].strftime('%Y-%m-%d %H:%M:%S,%f')[:-3]}")
        print(f"Total duration:  {stats['time_range_duration']}")
    else:
        print("No parsable timestamps found to determine range.")
    print("="*50 + "\n")


def print_filtered_logs(entries, max_lines=None):
    """
    Prints a list of filtered log entries.
    """
    print("\n" + "="*50)
    print(" " * 15 + "FILTERED LOG ENTRIES")
    print("="*50)
    if not entries:
        print("No log entries found matching the specified criteria.")
        print("="*50 + "\n")
        return

    count = 0
    for entry in entries:
        print(entry['raw_line'])
        count += 1
        if max_lines and count >= max_lines:
            print(f"\n--- Displaying first {max_lines} of {len(entries)} matching entries ---")
            break
    print(f"\nTotal matching entries: {len(entries)}")
    print("="*50 + "\n")


def main():
    """
    Main function to handle command-line arguments and run the log analysis.
    """
    parser = argparse.ArgumentParser(
        description="Analyze log files and extract statistics or filter entries.",
        formatter_class=argparse.RawTextHelpFormatter
    )

    parser.add_argument(
        "--file",
        "-f",
        required=True,
        help="Path to the log file to analyze."
    )
    parser.add_argument(
        "--level",
        "-l",
        help="Comma-separated list of log levels to filter (e.g., INFO, ERROR). "
             "If used with --stats, statistics will only include these levels."
    )
    parser.add_argument(
        "--keyword",
        "-k",
        help="Filter log entries containing this keyword in their message. Case-insensitive."
    )
    parser.add_argument(
        "--stats",
        "-s",
        action="store_true",
        help="Display only statistics (total lines, level distribution, time range). "
             "If omitted, matching log entries will be printed."
    )

    args = parser.parse_args()

    # Validate file existence early
    if not os.path.exists(args.file):
        print(f"Error: Log file not found at '{args.file}'", file=sys.stderr)
        sys.exit(1)
    
    # Process level filter argument
    level_filter_list = None
    if args.level:
        level_filter_list = [lvl.strip().upper() for lvl in args.level.split(',')]
        # Validate provided levels
        invalid_levels = [lvl for lvl in level_filter_list if lvl not in LogAnalyzer.VALID_LOG_LEVELS]
        if invalid_levels:
            print(f"Error: Invalid log levels provided: {', '.join(invalid_levels)}.", file=sys.stderr)
            print(f"Valid levels are: {', '.join(LogAnalyzer.VALID_LOG_LEVELS)}", file=sys.stderr)
            sys.exit(1)

    try:
        analyzer = LogAnalyzer(args.file)
        print(f"Analyzing log file: '{args.file}'...")
        analyzer.analyze()

        if analyzer.total_lines == 0:
            print("The log file is empty or no lines could be read.")
            sys.exit(0)

        if analyzer.parsed_lines == 0:
            print("No parsable log entries found in the file with the expected format.")
            print("Please ensure log lines match 'YYYY-MM-DD HH:MM:SS,ms [LEVEL] Message'.")
            sys.exit(0)

        if args.stats:
            # If --stats is present, print statistics based on filtered levels (if any)
            stats = analyzer.get_statistics(level_filter=level_filter_list)
            print_statistics(stats, filtered_levels=level_filter_list)
        else:
            # If --stats is not present, print filtered log entries
            filtered_entries = analyzer.get_filtered_logs(
                level_filter=level_filter_list,
                keyword_filter=args.keyword
            )
            print_filtered_logs(filtered_entries, max_lines=50) # Limit display to first 50 lines for brevity

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()