import re
import datetime
from collections import Counter
import os

class LogAnalyzer:
    """
    A utility class to parse and analyze log files.
    It can extract statistics and filter log entries based on level and keywords.
    """

    # Regex pattern to extract timestamp, log level, and message from a log line.
    # Assumes a format like: YYYY-MM-DD HH:MM:SS,ms [LEVEL] Message
    # Example: 2023-10-27 10:30:05,123 [INFO] User 'admin' logged in.
    LOG_PATTERN = re.compile(
        r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})"  # Timestamp: YYYY-MM-DD HH:MM:SS,ms
        r"\s\[(INFO|WARNING|ERROR|DEBUG|CRITICAL)\]"      # Log Level: [LEVEL]
        r"\s(.*)$"                                        # Message: Remaining part of the line
    )

    # Valid log levels for filtering
    VALID_LOG_LEVELS = {"INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"}

    def __init__(self, file_path):
        """
        Initializes the LogAnalyzer with the path to the log file.

        Args:
            file_path (str): The path to the log file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Log file not found: {file_path}")
        self.file_path = file_path
        self.total_lines = 0
        self.parsed_lines = 0
        self.log_level_counts = Counter()
        self.first_timestamp = None
        self.last_timestamp = None
        self.all_log_entries = [] # Store all parsed log entries for efficient filtering

    def _parse_line(self, line):
        """
        Parses a single log line using the predefined regex pattern.

        Args:
            line (str): A single line from the log file.

        Returns:
            tuple or None: A tuple (timestamp_obj, level, message) if the line matches the pattern,
                           otherwise None.
        """
        match = self.LOG_PATTERN.match(line)
        if match:
            timestamp_str, level, message = match.groups()
            try:
                # Parse timestamp string into a datetime object
                timestamp_obj = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")
                return timestamp_obj, level, message.strip()
            except ValueError:
                # Handle cases where timestamp format might be slightly off despite regex match
                return None
        return None

    def analyze(self):
        """
        Reads the log file, parses each line, and gathers initial statistics.
        Stores all successfully parsed log entries internally.
        """
        self.total_lines = 0
        self.parsed_lines = 0
        self.log_level_counts.clear()
        self.first_timestamp = None
        self.last_timestamp = None
        self.all_log_entries = []

        with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                self.total_lines += 1
                parsed_data = self._parse_line(line)
                if parsed_data:
                    timestamp, level, message = parsed_data
                    self.parsed_lines += 1
                    self.log_level_counts[level] += 1
                    self.all_log_entries.append({'timestamp': timestamp, 'level': level, 'message': message, 'raw_line': line.strip()})

                    # Update first and last timestamps
                    if self.first_timestamp is None or timestamp < self.first_timestamp:
                        self.first_timestamp = timestamp
                    if self.last_timestamp is None or timestamp > self.last_timestamp:
                        self.last_timestamp = timestamp

        if not self.all_log_entries:
            print(f"No parsable log entries found in '{self.file_path}'.")

    def get_filtered_logs(self, level_filter=None, keyword_filter=None):
        """
        Filters the parsed log entries based on specified log levels and keywords.

        Args:
            level_filter (list or None): A list of log levels (e.g., ['ERROR', 'WARNING'])
                                         to include. If None, all levels are included.
            keyword_filter (str or None): A keyword string. Only lines containing this
                                          keyword in their message will be included.
                                          Case-insensitive. If None, no keyword filter is applied.

        Returns:
            list: A list of dictionaries, where each dictionary represents a filtered log entry.
        """
        filtered_entries = []
        for entry in self.all_log_entries:
            match_level = True
            if level_filter:
                match_level = entry['level'] in level_filter

            match_keyword = True
            if keyword_filter:
                match_keyword = keyword_filter.lower() in entry['message'].lower()

            if match_level and match_keyword:
                filtered_entries.append(entry)
        return filtered_entries

    def get_statistics(self, level_filter=None):
        """
        Returns a dictionary containing statistical data of the log file.
        If a level_filter is provided, counts will only reflect those levels.

        Args:
            level_filter (list or None): A list of log levels to include in the statistics.
                                         If None, all levels are considered.

        Returns:
            dict: A dictionary with 'total_lines', 'parsed_lines', 'level_counts',
                  'first_timestamp', 'last_timestamp', and 'time_range_duration'.
        """
        filtered_level_counts = Counter()
        if level_filter:
            for level in level_filter:
                filtered_level_counts[level] = self.log_level_counts[level]
        else:
            filtered_level_counts = self.log_level_counts

        time_range_duration = None
        if self.first_timestamp and self.last_timestamp:
            time_range_duration = self.last_timestamp - self.first_timestamp

        return {
            'total_lines': self.total_lines,
            'parsed_lines': self.parsed_lines,
            'level_counts': filtered_level_counts,
            'first_timestamp': self.first_timestamp,
            'last_timestamp': self.last_timestamp,
            'time_range_duration': time_range_duration
        }