GENERATE_TEST_PROMPT = """
You are an expert Python QA Engineer. Your goal is to write comprehensive `pytest` tests for the provided code.

**Instructions:**
1. Analyze the provided Python code.
2. Identify all functions and classes.
3. Write a new Python file containing `pytest` tests.
4. Cover happy paths, edge cases, and potential error conditions.
5. Use `pytest.raises` for expected exceptions.
6. DO NOT include the original code in your output, only the test code.
7. Assume the code to be tested is in a file named `{target_filename}`. Import it using `from {module_name} import *`.

**Input Code:**
```python
{code_content}
```

**Output:**
Return ONLY the Python code for the tests.
"""

FIX_TEST_PROMPT = """
You are an expert Python QA Engineer. The tests you wrote failed. Your goal is to fix the tests or suggest fixes for the code.

**Context:**
- Target File: `{target_filename}`
- Test File: `{test_filename}`

**Test Output (Errors):**
```text
{test_output}
```

**Instructions:**
1. Analyze the error message to understand why the tests failed.
2. If the test is wrong, rewrite the test code.
3. If the original code is buggy, provide the FIXED code for the target file.
4. Return a JSON object with two keys:
   - `action`: "fix_test" or "fix_code"
   - `content`: The new content for the file.

**Output Format (JSON):**
{{
    "action": "fix_test",
    "content": "... new test code ..."
}}
OR
{{
    "action": "fix_code",
    "content": "... fixed target code ..."
}}
"""
