import os
from pathlib import Path
import os.path, time
import datetime
import random

#import csv

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
        self.char = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        )


    def get_external_storage_directory(self) -> Path:
        """
        Get the external storage directory for Android or fallback to current directory.
        For Android, we check common environment variables.
        """
        if("ANDROID_BOOTLOGO" in os.environ):
            storage_dir = ""
            return Path(storage_dir)

        storage_dir = os.getenv("EXTERNAL_STORAGE") or os.getenv("HOME")
        if storage_dir is None:
            storage_dir = ""
        return Path(storage_dir)

    
    def get_file_path(self, filename: str) -> Path:
        """Returns the full path of a file."""
        if("ANDROID_BOOTLOGO" in os.environ):            
            return self.base_path / filename
        else:
            print(f"base path {self.base_path / ("src/" + filename)}")
            return self.base_path / ("src/" + filename)


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
        with open(file_path, "r") as file:
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

        lines[line - 1] = str(value) + '\n'

        with open(file_path, "w") as file:
            file.writelines(lines)


    def matrix_csv(self, path):
        main = []
        file_path = self.get_file_path(path)
        with open(file_path, 'r') as file:
            for line in file:
                if "id," not in line:                
                    main.append(line.split(','))
        return main

    def rl_csv(self, path, id):
        file_path = self.get_file_path(path)
        with open(file_path, 'r') as file:
            for line in file:
                if id in line:
                    return line.split(',')[id]


    def app_csv(self, path, value):
        file_path = self.get_file_path(path)        
        with open(file_path, 'a', newline='') as fileTemp:
            csvwriter = csv.writer(fileTemp)
            csvwriter.writerow(value)

    def uniq_id(self):
        return ''.join(random.choice(self.char) for _ in range(10))
