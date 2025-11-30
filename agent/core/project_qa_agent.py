import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from agent.tools.file_ops import read_file, write_file, list_files
from agent.tools.test_runner import run_pytest
from agent.prompts.qa_prompts import PROJECT_SCAN_PROMPT, INTEGRATION_TEST_PROMPT

class ProjectQAAgent:
    def __init__(self, root_dir: str = "."):
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"
        self.root_dir = root_dir
        self.test_dir = os.path.join(root_dir, "tests", "integration")

    def scan_project(self):
        """Scans the project structure and identifies integration scenarios."""
        print(f"🔍 Scanning project in {self.root_dir}...")
        all_files = list_files(self.root_dir)
        
        # Create a summary of files (name + first few lines maybe? for now just names)
        file_list_str = "\n".join(all_files)
        
        prompt = PROJECT_SCAN_PROMPT.format(file_list=file_list_str)
        
        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )

        try:
            analysis = json.loads(response.text)
            print(f"✅ Project Analysis: {analysis.get('project_type', 'Unknown')}")
            return analysis
        except json.JSONDecodeError:
            print("❌ Failed to parse project analysis.")
            return None

    def generate_integration_tests(self, analysis: dict):
        """Generates integration tests based on the analysis."""
        if not analysis:
            return

        os.makedirs(self.test_dir, exist_ok=True)
        scenarios = analysis.get("integration_scenarios", [])
        
        for scenario in scenarios:
            print(f"⚙️ Generating test for scenario: {scenario['name']}...")
            
            # Gather context from involved modules
            code_context = ""
            for module_name in scenario.get("involved_modules", []):
                # Simple heuristic to find file path from module name
                # This might need improvement for complex paths
                file_path = self._find_file(module_name)
                if file_path:
                    content = read_file(file_path)
                    code_context += f"\n# File: {file_path}\n{content}\n"
            
            prompt = INTEGRATION_TEST_PROMPT.format(
                scenario_name=scenario['name'],
                scenario_description=scenario['description'],
                code_context=code_context
            )

            response = self.client.models.generate_content(
                model=self.model,
                contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
            )
            
            test_code = self._extract_code(response.text)
            safe_name = scenario['name'].lower().replace(" ", "_")
            test_file_path = os.path.join(self.test_dir, f"test_integration_{safe_name}.py")
            
            write_file(test_file_path, test_code)
            print(f"  -> Created {test_file_path}")

    def run_full_suite(self):
        """Runs all tests in the integration directory."""
        print("\n🚀 Running full integration suite...")
        result = run_pytest(self.test_dir)
        if result["success"]:
            print("🎉 All integration tests passed!")
        else:
            print("❌ Some tests failed.")
            # print(result["stdout"])

    def _find_file(self, module_name: str) -> str:
        """Helper to find a file path given a module name (fuzzy match)."""
        # This is a simplified lookup. In a real project, we'd parse imports.
        # Here we just look for a file that ends with module_name.py
        all_files = list_files(self.root_dir)
        for f in all_files:
            if f.endswith(f"{module_name}.py") or f.endswith(f"/{module_name}.py"):
                return f
            # Handle cases where module_name might be 'agent.core.qa_agent'
            parts = module_name.split(".")
            if f.endswith(os.path.join(*parts) + ".py"):
                return f
        return None

    def _extract_code(self, text: str) -> str:
        """Helper to extract code from markdown blocks."""
        if "```python" in text:
            return text.split("```python")[1].split("```")[0].strip()
        elif "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text
