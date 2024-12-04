import os
from pathlib import Path

class FileSystem:
    def __init__(self):
        # Use an external directory or fallback to the current directory
        self.base_path = self.get_external_storage_directory()

    def get_external_storage_directory(self) -> Path:
        """Get the external storage directory for Android or fallback to current directory."""
        # For Android, you can specify external storage paths
        storage_dir = os.getenv("EXTERNAL_STORAGE") or os.getenv("HOME") or "."
        return Path(storage_dir)

    def get_file_path(self, filename: str) -> Path:
        """Returns the full path of a file."""
        return self.base_path / filename

    def write_to_file(self, filename: str, content: str) -> str:
        """Writes content to a file and returns the file path."""
        file_path = self.get_file_path(filename)
        with open(file_path, "w") as file:
            file.write(content)
        return str(file_path)

    def read_from_file(self, filename: str) -> str:
        """Reads and returns content from a file, or an error message."""
        file_path = self.get_file_path(filename)
        if file_path.exists():
            with open(file_path, "r") as file:
                return file.read()
        else:
            return f"Error: {filename} not found."

    def file_exists(self, filename: str) -> bool:
        """Checks if a file exists."""
        return self.get_file_path(filename).exists()


    def read_given_line(self, filename, line):
        with open(filename, "r") as file:
            return file.readlines()[line]

    def append_file(self, value, line, path):    
        file_path = self.get_file_path(path)        
        with open(file_path, 'r') as file:
            lines = file.readlines()

        lines[line - 1] = value + '\n'

        with open(file_path, 'w') as file:
            file.writelines(lines)
