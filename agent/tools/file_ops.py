import os

def read_file(file_path: str) -> str:
    """Reads the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file {file_path}: {e}"

def write_file(file_path: str, content: str) -> str:
    """Writes content to a file. Creates directories if they don't exist."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {file_path}"
    except Exception as e:
        return f"Error writing to {file_path}: {e}"

def list_files(directory: str = ".") -> list[str]:
    """Lists all files in a directory recursively."""
    file_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py") and "__pycache__" not in root:
                 file_list.append(os.path.join(root, file))
    return file_list
