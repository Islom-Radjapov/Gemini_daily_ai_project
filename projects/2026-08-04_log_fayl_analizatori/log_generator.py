import datetime
import random
import time
import os

def generate_sample_log(filename="sample.log", num_entries=1000):
    """
    Generates a sample log file with various log levels and messages.

    Args:
        filename (str): The name of the log file to generate.
        num_entries (int): The number of log entries to create.
    """
    log_levels = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]
    messages = [
        "User 'admin' logged in successfully.",
        "Database connection established.",
        "Attempted to connect to external service.",
        "Request processed in {}ms.",
        "File '{}' not found, retrying.",
        "Invalid input received from user {}.",
        "Configuration reloaded.",
        "Memory usage exceeded threshold: {}MB.",
        "Worker process started.",
        "Authentication failed for user '{}'.",
        "Disk space low: {}% remaining.",
        "Network timeout during API call to {}.",
        "Scheduled task 'cleanup' completed.",
        "Unhandled exception in module '{}'."
    ]
    
    # Ensure a mix of timestamps
    start_time = datetime.datetime.now() - datetime.timedelta(days=1, hours=random.randint(0,23))

    print(f"Generating {num_entries} log entries into '{filename}'...")

    with open(filename, 'w', encoding='utf-8') as f:
        for i in range(num_entries):
            current_time = start_time + datetime.timedelta(seconds=i * random.uniform(0.1, 5))
            current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S,%f")[:-3] # Truncate microseconds to milliseconds

            level = random.choice(log_levels)
            
            # Make some messages more likely to contain specific keywords
            if level == "ERROR" and random.random() < 0.7:
                msg_template = random.choice([
                    "Database connection failed.",
                    "Failed to process request for user {}",
                    "Unhandled exception: {}",
                    "Error occurred during file operation on '{}'."
                ])
                message = msg_template.format(random.choice(['prod_db', 'user_data', 'SystemError', '/var/log/app.log']))
            elif level == "WARNING" and random.random() < 0.6:
                msg_template = random.choice([
                    "Low disk space warning: {}% free.",
                    "Slow query detected: {}ms.",
                    "External service 'analytics' responded slowly."
                ])
                message = msg_template.format(random.randint(5,15))
            elif level == "CRITICAL":
                message = random.choice([
                    "System shutdown initiated due to critical error.",
                    "Security breach detected in authentication module.",
                    "Out of memory: process terminated."
                ])
            else:
                msg_template = random.choice(messages)
                # Fill placeholders
                if '{}' in msg_template:
                    if "user" in msg_template:
                        message = msg_template.format(random.choice(['john.doe', 'jane.smith', 'admin', 'guest']))
                    elif "file" in msg_template:
                        message = msg_template.format(random.choice(['config.ini', 'data.json', 'image.png']))
                    elif "ms" in msg_template:
                        message = msg_template.format(random.randint(10, 5000))
                    elif "MB" in msg_template:
                        message = msg_template.format(random.randint(100, 2000))
                    elif "%" in msg_template:
                        message = msg_template.format(random.randint(1, 100))
                    elif "API" in msg_template:
                        message = msg_template.format(random.choice(['api.example.com', 'payment.gateway.net']))
                    elif "module" in msg_template:
                        message = msg_template.format(random.choice(['auth_module', 'data_processor', 'web_server']))
                    else:
                        message = msg_template.format("placeholder_value")
                else:
                    message = msg_template

            log_line = f"{current_time_str} [{level}] {message}\n"
            f.write(log_line)
    
    print(f"Successfully generated '{filename}' with {num_entries} entries.")
    print("You can now run 'python main.py --file sample.log --stats' to analyze it.")

if __name__ == "__main__":
    generate_sample_log()