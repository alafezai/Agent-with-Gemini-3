import sys
import os
from agent.core.qa_agent import QAAgent

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_to_test.py>")
        sys.exit(1)

    target_file = sys.argv[1]
    
    if not os.path.exists(target_file):
        print(f"Error: File '{target_file}' not found.")
        sys.exit(1)

    print(f"🚀 Starting QA Agent on {target_file}...")
    
    try:
        agent = QAAgent()
        success = agent.run(target_file)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
