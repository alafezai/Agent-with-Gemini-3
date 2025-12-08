import pytest
import os
from unittest.mock import patch
from agent.core.qa_agent import QAAgent
from agent.tools.codebase_analyzer import CodebaseAnalyzer
from agent.tools.test_generator import TestGenerator
from agent.tools.test_runner import TestRunner
from agent.tools import file_ops

@pytest.fixture
def qa_agent(tmpdir):
    """Fixture to create a QAAgent instance with a temporary directory."""
    project_dir = str(tmpdir.mkdir("project"))
    return QAAgent(project_dir=project_dir)

@pytest.fixture
def sample_code(tmpdir):
    """Fixture to create a sample code file."""
    project_dir = str(tmpdir.mkdir("sample_project"))
    file_path = os.path.join(project_dir, "sample.py")
    with open(file_path, "w") as f:
        f.write("def add(x, y):\n  return x + y\n")
    return project_dir, file_path

def test_qa_agent_end_to_end(qa_agent, sample_code, tmpdir):
    """
    Integration test for the QAAgent's end-to-end execution flow.
    """
    project_dir, file_path = sample_code
    qa_agent.project_dir = project_dir # Ensure agent uses the correct directory

    with patch("agent.tools.codebase_analyzer.CodebaseAnalyzer.analyze_codebase") as mock_analyze:
        mock_analyze.return_value = "Simple addition function" # Minimal analysis result

        with patch("agent.tools.test_generator.TestGenerator.generate_tests") as mock_generate:
            test_file_path = os.path.join(project_dir, "test_sample.py")
            mock_generate.return_value = test_file_path
            with open(test_file_path, "w") as f:
                f.write("def test_add():\n  assert 1 + 1 == 2\n")

            with patch("agent.tools.test_runner.TestRunner.run_tests") as mock_run:
                mock_run.return_value = {"passed": 1, "failed": 0}

                results = qa_agent.run()

                assert "analysis" in results
                assert "tests_generated" in results
                assert "test_results" in results
                assert results["analysis"] == "Simple addition function"
                assert results["tests_generated"] == test_file_path
                assert results["test_results"]["passed"] == 1
                assert results["test_results"]["failed"] == 0

def test_qa_agent_flow_no_tests_needed(qa_agent, sample_code):
    """
    Integration test when the codebase analyzer determines no tests are needed.
    """
    project_dir, file_path = sample_code
    qa_agent.project_dir = project_dir

    with patch("agent.tools.codebase_analyzer.CodebaseAnalyzer.analyze_codebase") as mock_analyze:
        mock_analyze.return_value = "No tests needed."

        results = qa_agent.run()

        assert "analysis" in results
        assert "tests_generated" not in results
        assert "test_results" not in results
        assert results["analysis"] == "No tests needed."