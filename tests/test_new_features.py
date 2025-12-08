import sys
import os

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from agent.core.project_qa_agent import ProjectQAAgent

def test_memory():
    print("Testing Memory...")
    agent = ProjectQAAgent()
    agent.memory.add_message("user", "Hello")
    history = agent.memory.get_history()
    assert len(history) == 1
    assert history[0]["content"] == "Hello"
    print("✅ Memory test passed")

def test_search_tool():
    print("Testing Search Tool...")
    agent = ProjectQAAgent()
    # Search for something we know exists, like "ConversationMemory" in the file we just made
    results = agent.search_code("ConversationMemory")
    assert len(results) > 0
    found = any("conversation_memory.py" in r for r in results)
    assert found
    print("✅ Search tool test passed")

def test_system_tool():
    print("Testing System Tool...")
    agent = ProjectQAAgent()
    # Run a simple echo command
    output = agent.execute_system_command("echo Hello World")
    assert "Hello World" in output
    print("✅ System tool test passed")

if __name__ == "__main__":
    try:
        test_memory()
        test_search_tool()
        test_system_tool()
        print("\n🎉 All new feature tests passed!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        sys.exit(1)
