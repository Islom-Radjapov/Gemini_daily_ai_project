import sys
from cron_explainer import cron_parser

def main():
    """
    Main function to run the cron explainer utility from the command line.
    It takes a cron expression as a command-line argument and prints its explanation.
    """
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<cron_expression>\"")
        print("Example: python main.py \"* 10 * * MON-FRI\"")
        print("Example: python main.py \"0 0 1,15 * 6\"")
        sys.exit(1)

    cron_expression = sys.argv[1]
    
    # Explain the cron expression using the cron_parser module
    explanation_result = cron_parser.explain_cron_expression(cron_expression)
    
    print("\n--- Cron Expression Explanation ---")
    print(f"Expression: {cron_expression}\n")
    
    # Print the high-level summary
    print(f"Summary: {explanation_result['summary']}\n")
    
    # Print detailed explanations for each field
    print("Details:")
    for detail in explanation_result['details']:
        print(detail)
    print("-----------------------------------\n")

if __name__ == "__main__":
    main()