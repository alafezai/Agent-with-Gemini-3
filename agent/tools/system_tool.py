import subprocess

def run_command(command: str) -> str:
    """
    Executes a system command and returns the output.
    """
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=60  # Safety timeout
        )
        output = f"Stdout:\n{result.stdout}\n"
        if result.stderr:
            output += f"Stderr:\n{result.stderr}\n"
        return output
    except Exception as e:
        return f"Error executing command '{command}': {e}"
