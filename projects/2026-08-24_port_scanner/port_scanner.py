import socket
import argparse
import sys
import time
from concurrent.futures import ThreadPoolExecutor
import os

# ANSI escape codes for colored output
# These will work on most modern terminals (Linux, macOS, Windows 10+)
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BLUE = "\033[94m"
CYAN = "\033[96m"

def display_message(message, color=RESET, file=sys.stdout):
    """
    Displays a message to the console with optional color.
    Checks if the output is a TTY to decide whether to apply colors.
    """
    if file.isatty(): # Only apply colors if output is to a terminal
        print(f"{color}{message}{RESET}", file=file)
    else:
        print(message, file=file)

def scan_port(target_ip, port, timeout):
    """
    Attempts to connect to a specific port on the target IP.
    Returns True if the port is open, False otherwise.
    """
    try:
        # Create a new socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set a timeout for the connection attempt
        sock.settimeout(timeout)
        # Attempt to connect to the target IP and port
        # connect_ex returns 0 on success, otherwise an error code
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            # Port is open
            return True
        else:
            # Port is closed or filtered
            return False
    except socket.error as e:
        # Handle socket-related errors (e.g., network unreachable, permissions)
        # For a port scanner, any error preventing a successful connection
        # means the port is effectively not open from our perspective.
        return False
    finally:
        # Ensure the socket is closed to prevent resource leaks
        if 'sock' in locals() and sock:
            sock.close()

def parse_ports(ports_str):
    """
    Parses a string representing ports into a list of integers.
    Supports single ports (e.g., "80") or ranges (e.g., "1-1024").
    Returns a list of port integers.
    """
    port_list = []
    
    # If no ports are specified, use a list of common ports
    if not ports_str:
        display_message("No ports specified. Scanning common ports: 20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3389, 8080", YELLOW)
        return [20, 21, 22, 23, 25, 53, 80, 110, 135, 139, 443, 445, 3389, 8080]

    if '-' in ports_str:
        # Handle port ranges like "1-1024"
        try:
            start_port, end_port = map(int, ports_str.split('-'))
            if not (1 <= start_port <= 65535 and 1 <= end_port <= 65535 and start_port <= end_port):
                raise ValueError("Port range must be between 1-65535 and start_port must be less than or equal to end_port.")
            port_list.extend(range(start_port, end_port + 1))
        except ValueError as e:
            display_message(f"Error: Invalid port range '{ports_str}'. {e}", RED, sys.stderr)
            sys.exit(1)
    else:
        # Handle single port like "80"
        try:
            port = int(ports_str)
            if not (1 <= port <= 65535):
                raise ValueError("Port number must be between 1 and 65535.")
            port_list.append(port)
        except ValueError as e:
            display_message(f"Error: Invalid port number '{ports_str}'. {e}", RED, sys.stderr)
            sys.exit(1)
    
    return port_list

def main():
    """
    Main function to parse arguments and initiate the port scan.
    """
    parser = argparse.ArgumentParser(
        description=f"{BLUE}Python Port Scanner Utility{RESET}",
        formatter_class=argparse.RawTextHelpFormatter # Allows for newlines in help text
    )
    parser.add_argument(
        '-t', '--target', 
        required=True, 
        help='Target host or IP address (e.g., example.com, 192.168.1.1)'
    )
    parser.add_argument(
        '-p', '--ports', 
        default=None, # Set default to None to trigger common ports logic
        help='Ports to scan. Can be a single port (e.g., "80") or a range (e.g., "1-1024").\n'
             'If not specified, a list of common ports will be scanned.'
    )
    parser.add_argument(
        '-w', '--workers', 
        type=int, 
        default=os.cpu_count() * 5 if os.cpu_count() else 50, # Dynamic default based on CPU cores
        help='Number of worker threads for scanning (default: based on CPU cores, min 50)'
    )
    parser.add_argument(
        '-o', '--timeout', 
        type=float, 
        default=1.0, 
        help='Connection timeout in seconds for each port (default: 1.0)'
    )

    args = parser.parse_args()

    display_message(f"\n[{BLUE}--- Python Port Scanner ---{RESET}]")
    display_message(f"Target: {args.target}", CYAN)
    display_message(f"Timeout per port: {args.timeout} seconds", CYAN)
    display_message(f"Worker threads: {args.workers}", CYAN)

    try:
        # Resolve target host to its IP address
        target_ip = socket.gethostbyname(args.target)
        display_message(f"Resolved IP: {target_ip}", CYAN)
    except socket.gaierror:
        display_message(f"Error: Could not resolve target host '{args.target}'. Please check the hostname or IP address.", RED, sys.stderr)
        sys.exit(1)
    
    # Parse the ports specified by the user
    ports_to_scan = parse_ports(args.ports)

    if not ports_to_scan:
        display_message("No ports to scan after parsing. Exiting.", RED, sys.stderr)
        sys.exit(1)

    display_message(f"Scanning {len(ports_to_scan)} ports...", BLUE)
    display_message("-" * 40, BLUE)
    display_message("Open Ports:", GREEN)
    
    start_time = time.time()
    
    # Use ThreadPoolExecutor for concurrent scanning to improve speed
    open_ports_found = 0
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        # Submit scan_port tasks for all ports
        # The map function would return results in order, but we want to process
        # them as they complete. `as_completed` is more suitable for this.
        futures = {executor.submit(scan_port, target_ip, port, args.timeout): port for port in ports_to_scan}
        
        # Iterate over futures as they complete
        for future in concurrent.futures.as_completed(futures):
            port = futures[future] # Get the original port number from the future
            try:
                if future.result():
                    display_message(f"  Port {port} is OPEN", GREEN)
                    open_ports_found += 1
            except Exception as exc:
                # Catch any unexpected exceptions that might occur during the scan_port execution
                display_message(f"  Port {port} generated an unexpected exception: {exc}", YELLOW, sys.stderr)

    end_time = time.time()
    
    display_message("-" * 40, BLUE)
    if open_ports_found == 0:
        display_message("No open ports found.", YELLOW)
    else:
        display_message(f"Found {open_ports_found} open port(s).", GREEN)
    display_message(f"Scan completed in {end_time - start_time:.2f} seconds.", BLUE)
    display_message(f"[{BLUE}--- Scan Finished ---{RESET}]")

if __name__ == "__main__":
    main()