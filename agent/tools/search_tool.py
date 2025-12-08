import os

def search_in_files(query: str, directory: str = ".") -> list[str]:
    """
    Searches for a string in all files within a directory.
    Returns a list of strings formatted as 'file_path:line_number: content'.
    """
    results = []
    for root, _, files in os.walk(directory):
        if "__pycache__" in root or ".git" in root or ".venv" in root:
            continue
            
        for file in files:
            try:
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    for i, line in enumerate(f, 1):
                        if query in line:
                            results.append(f"{file_path}:{i}: {line.strip()}")
            except Exception:
                # Ignore files that can't be read
                continue
    return results
