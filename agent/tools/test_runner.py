import subprocess
import sys

def run_pytest(test_file: str = None) -> dict:
    """
    Runs pytest on a specific file or the whole directory.
    Returns a dictionary with success status and output.
    """
    command = [sys.executable, "-m", "pytest"]
    if test_file:
        command.append(test_file)
    
    # Capture output to analyze later
    result = subprocess.run(
        command, 
        capture_output=True, 
        text=True
    )
    
    return {
        "success": result.returncode == 0,
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
