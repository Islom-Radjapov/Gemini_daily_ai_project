import http.server
import socketserver
import os
import sys
import argparse
from datetime import datetime

# Default configuration for the server
DEFAULT_PORT = 8000
DEFAULT_DIRECTORY = "web_content"

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """
    A custom HTTP request handler that extends SimpleHTTPRequestHandler.
    It provides custom error pages (404, 403, etc.) if corresponding HTML files exist
    in the serving directory. It also customizes the logging format.
    """

    def log_message(self, format, *args):
        """
        Overrides the default log_message to provide a more detailed and
        standardized server log format, including the timestamp.
        Example format: "127.0.0.1 - - [2023-10-27 10:30:00] "GET /index.html HTTP/1.1" 200 -"
        """
        sys.stdout.write("%s - - [%s] %s\n" %
                         (self.address_string(),
                          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                          format % args))

    def send_error(self, code, message=None, explain=None):
        """
        Sends an error response.
        Attempts to serve a custom error page (e.g., 404.html, 403.html)
        from the current working directory if available.
        Falls back to the default SimpleHTTPRequestHandler error page otherwise.
        """
        try:
            # Construct the path to the custom error page
            error_page_name = f"{code}.html"
            error_page_path = os.path.join(os.getcwd(), error_page_name)

            # Check if the custom error page exists
            if os.path.exists(error_page_path):
                self.send_response(code)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(error_page_path, 'rb') as f:
                    self.wfile.write(f.read())
                self.log_message("Served custom error page: %s for status %d", error_page_name, code)
                return
        except Exception as e:
            # Log any errors encountered while trying to serve a custom error page
            self.log_error("Error serving custom error page '%s': %s", error_page_name, e)

        # Fallback to default SimpleHTTPRequestHandler error page
        super().send_error(code, message, explain)

def main():
    """
    Main function to parse arguments and start the HTTP server.
    """
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="A simple, custom Python HTTP server to serve static files.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=DEFAULT_PORT,
        help="Port number to serve HTTP requests on."
    )
    parser.add_argument(
        "--directory", "-d",
        type=str,
        default=DEFAULT_DIRECTORY,
        help="Directory from which to serve files. The server will change its CWD to this directory."
    )

    args = parser.parse_args()

    serving_directory = os.path.abspath(args.directory)
    port = args.port

    # Validate the serving directory
    if not os.path.isdir(serving_directory):
        print(f"Error: Serving directory '{serving_directory}' not found or is not a directory.", file=sys.stderr)
        sys.exit(1)

    # Change the current working directory to the specified serving directory.
    # This is crucial for SimpleHTTPRequestHandler to find and serve files
    # correctly, and also for finding custom error pages.
    os.chdir(serving_directory)

    # Set the request handler for the server
    Handler = CustomHTTPRequestHandler

    # Create and start the TCP server
    try:
        with socketserver.TCPServer(("", port), Handler) as httpd:
            print(f"==================================================")
            print(f"🚀 Starting Python HTTP Server 🚀")
            print(f"Serving files from directory: '{serving_directory}'")
            print(f"Listening on port: {port}")
            print(f"Access it at: http://localhost:{port}/")
            print(f"Press Ctrl+C to stop the server.")
            print(f"==================================================")

            httpd.serve_forever() # Run the server indefinitely

    except OSError as e:
        if e.errno == 98: # Address already in use
            print(f"Error: Port {port} is already in use.", file=sys.stderr)
            print("Please choose a different port using the --port argument.", file=sys.stderr)
        else:
            print(f"An OS error occurred: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        # Handle graceful shutdown on Ctrl+C
        print("\n==================================================")
        print("🛑 Shutting down server...")
        httpd.shutdown() # Cleanly stop the server
        print("Server gracefully stopped. Goodbye! 👋")
        print("==================================================")
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()