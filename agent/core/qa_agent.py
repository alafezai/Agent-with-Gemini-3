import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

from agent.tools.file_ops import read_file, write_file
from agent.tools.test_runner import run_pytest
from agent.prompts.qa_prompts import GENERATE_TEST_PROMPT, FIX_TEST_PROMPT

class QAAgent:
    def __init__(self):
        load_dotenv()
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")
        self.client = genai.Client(api_key=api_key)
        self.model = "gemini-2.0-flash"

    def generate_tests(self, target_file: str, test_file: str):
        """Generates initial tests for a file."""
        print(f"🔍 Analyzing {target_file}...")
        code_content = read_file(target_file)
        
        module_name = os.path.splitext(os.path.basename(target_file))[0]
        prompt = GENERATE_TEST_PROMPT.format(
            target_filename=target_file,
            module_name=module_name,
            code_content=code_content
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])]
        )
        
        # Extract code block if present
        test_code = self._extract_code(response.text)
        write_file(test_file, test_code)
        print(f"✅ Generated tests in {test_file}")

    def fix_tests(self, target_file: str, test_file: str, test_output: str):
        """Attempts to fix tests or code based on errors."""
        print("🔧 Attempting to fix...")
        prompt = FIX_TEST_PROMPT.format(
            target_filename=target_file,
            test_filename=test_file,
            test_output=test_output
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=[types.Content(role="user", parts=[types.Part(text=prompt)])],
            config=types.GenerateContentConfig(response_mime_type="application/json")
        )

        try:
            result = json.loads(response.text)
            action = result.get("action")
            content = result.get("content")

            if action == "fix_test":
                write_file(test_file, content)
                print("📝 Updated test file.")
            elif action == "fix_code":
                write_file(target_file, content)
                print("📝 Updated target code file.")
            else:
                print(f"⚠️ Unknown action: {action}")
        except json.JSONDecodeError:
            print("❌ Failed to parse JSON response from Gemini.")

    def run(self, target_file: str, max_retries: int = 3):
        """Main loop."""
        test_dir = "tests"
        os.makedirs(test_dir, exist_ok=True)
        test_file = os.path.join(test_dir, f"test_{os.path.basename(target_file)}")

        # 1. Generate initial tests
        self.generate_tests(target_file, test_file)

        # 2. Loop: Run -> Fix -> Repeat
        for i in range(max_retries):
            print(f"\n🏃 Running tests (Attempt {i+1}/{max_retries})...")
            result = run_pytest(test_file)

            if result["success"]:
                print("🎉 All tests passed!")
                return True
            
            print("❌ Tests failed.")
            # print(result["stdout"]) # Optional: print full log
            
            if i < max_retries - 1:
                self.fix_tests(target_file, test_file, result["stdout"] + result["stderr"])
            else:
                print("🛑 Max retries reached. Tests still failing.")
        
        return False

    def _extract_code(self, text: str) -> str:
        """Helper to extract code from markdown blocks."""
        if "```python" in text:
            return text.split("```python")[1].split("```")[0].strip()
        elif "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text
