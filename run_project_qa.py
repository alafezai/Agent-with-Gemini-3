import sys
import os

# Add the current directory to sys.path to ensure imports work
sys.path.append(os.getcwd())

from agent.core.project_qa_agent import ProjectQAAgent

def main():
    print("🤖 Starting Project QA Agent...")
    
    # Initialize agent pointing to the current directory
    agent = ProjectQAAgent(root_dir=".")
    
    # 1. Scan the project
    analysis = agent.scan_project()
    
    if not analysis:
        print("❌ Project analysis failed.")
        return

    # 2. Generate Integration Tests
    agent.generate_integration_tests(analysis)
    
    # 3. Run the tests
    agent.run_full_suite()

if __name__ == "__main__":
    main()
