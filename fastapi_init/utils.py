import os
import logging

# Set up logger
logger = logging.getLogger(__name__)

def log_message(message: str) -> None:
    """Log a message to the console."""
    print(f"[LOG] {message}")

def validate_project_name(name: str) -> bool:
    """Validate the project name according to certain rules."""
    if not name.isidentifier():
        log_message("Invalid project name. It must be a valid Python identifier.")
        return False
    return True

def read_file(file_path: str) -> str:
    """Read the contents of a file and return it as a string."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def write_file(file_path: str, content: str) -> None:
    """Write content to a file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def ensure_directory_exists(directory_path: str) -> None:
    """Ensure that a directory exists; create it if it does not."""
    os.makedirs(directory_path, exist_ok=True)