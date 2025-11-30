import pytest
from unittest.mock import patch
import os

from agent.core.qa_agent import QAAgent
from agent.tools.code_explorer import CodeExplorer
from agent.tools.file_ops import FileOps
from agent.tools.test_generator import TestGenerator
from agent.tools.test_executor import TestExecutor

@pytest.fixture
def qa_agent():
    """Fixture to create a QA Agent instance."""
    code_explorer = CodeExplorer()
    file_ops = FileOps()
    test_generator = TestGenerator()
    test_executor = TestExecutor()
    return QAAgent(code_explorer, file_ops, test_generator, test_executor)


def create_dummy_file(filename, content):
    """Helper function to create a dummy file for testing."""
    with open(filename, "w") as f:
        f.write(content)


def delete_dummy_file(filename):
    """Helper function to delete a dummy file after testing."""
    try:
        os.remove(filename)
    except FileNotFoundError:
        pass

@pytest.mark.integration
def test_qa_agent_assisted_code_understanding_and_testing(qa_agent, tmp_path):
    """
    Integration test for QA Agent assisted code understanding and testing.

    This test creates a dummy Python file, asks the QA Agent to understand it,
    generate tests, and execute them.
    """

    # 1. Create a dummy Python file
    dummy_file_path = tmp_path / "dummy_module.py"
    dummy_file_content = """
def add(a, b):
    \"\"\"Adds two numbers.\"\"\"
    return a + b

def subtract(a, b):
    \"\"\"Subtracts two numbers.\"\"\"
    return a - b
"""
    create_dummy_file(dummy_file_path, dummy_file_content)

    # 2. Mock external dependencies (if any, TestExecutor might use subprocess)
    # No external dependencies to mock in this scenario given available context.

    # 3. Instruct the QA Agent to understand the code and generate tests
    code_understanding_task = f"Please analyze the code in {dummy_file_path} and generate pytest tests for it."
    analysis_result = qa_agent.analyze_code_and_generate_tests(str(dummy_file_path), code_understanding_task)

    # Assert that the test generation was successful (at least some content was generated)
    assert analysis_result is not None
    assert "test_" in analysis_result
    assert "def test_add" in analysis_result # Check if test generated includes an add test
    assert "def test_subtract" in analysis_result # Check if test generated includes an subtract test


    # 4. Write the generated test to a file
    test_file_path = tmp_path / "test_dummy_module.py"
    create_dummy_file(test_file_path, analysis_result)


    # 5. Execute the generated tests
    execution_result = qa_agent.test_executor.execute_tests(str(test_file_path))

    # 6. Assert that the tests passed (this is a simplified assertion, more robust checks might be needed)
    assert "passed" in execution_result.lower()

    # Clean up the dummy files
    delete_dummy_file(dummy_file_path)
    delete_dummy_file(test_file_path)