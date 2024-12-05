import os
from pathlib import Path
import os.path, time
import datetime

class FileSystem:
    def __init__(self):
        # Use an external directory or fallback to the current directory
        self.base_path = self.get_external_storage_directory()
        self.equivalent_mo = {
            'Jan': 1,
            'Feb': 2,
            'Mar': 3,
            'Apr': 4,
            'May': 5,
            'Jun': 6,
            'Jul': 7,
            'Aug': 8,
            'Sep': 9, 
            'Oct': 10,
            'Nov': 11,
            'Dec': 12
    }

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
        file_path = self.get_file_path(filename)
        with open(filename, "r") as file:
            return file.readlines()[line]

    def get_last_modified(self):
        doc_path = self.get_file_path("./document/")
        latest_time = datetime.datetime.min  # Initialize to the earliest possible datetime
        latest_path = ""

        for root, dirs, files in os.walk(doc_path):
            for file in files:
                file_full_path = os.path.join(root, file)
                file_mtime = datetime.datetime.fromtimestamp(os.path.getmtime(file_full_path))

                # Debugging information
                print(f"File: {file}, Modified Time: {file_mtime}")

                if file_mtime > latest_time:
                    latest_time = file_mtime
                    latest_path = file_full_path

        #print("Latest File Path:", latest_path)
        #print("Latest File Name:", os.path.basename(latest_path))
        return os.path.basename(latest_path)  


    def append_file(self, value, line, path):    
        file_path = self.get_file_path(path)        
        with open(file_path, 'r') as file:
            lines = file.readlines()

        lines[line - 1] = value + '\n'

        with open(file_path, 'w') as file:
            file.writelines(lines)
