import os
from pathlib import Path
import os.path, time
import datetime
import random

import csv

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
        if("ANDROID_BOOTLOGO" in os.environ):
            storage_dir = ""
            return Path(storage_dir)

        storage_dir = os.getenv("EXTERNAL_STORAGE") or os.getenv("HOME")
        if storage_dir is None:
            storage_dir = ""
        return Path(storage_dir)

    
    def get_file_path(self, filename: str) -> Path:
        if("ANDROID_BOOTLOGO" in os.environ):            
            return self.base_path / filename
        else:
            print(f"base path {self.base_path / ("src/" + filename)}")
            return self.base_path / ("src/" + filename)

    def is_empty(self, filename) -> bool:
        file_path = self.get_file_path(filename)    
        if os.path.getsize(file_path) == 0:
            return True
        return False

    def write_csv(self, filename, data):
        file_path = self.get_file_path(filename)
        with open(file_path, "a") as file:
            writer = csv.writer(file)
            writer.writerows(data)

    def read_csv(self, filename):
        file_path = self.get_file_path(filename)
        try:
            with open(file_path, "r") as file:
                reader = csv.reader(file)
                return [row for row in reader]
        except FileNotFoundError:
            print(f"not foud {FileNotFoundError}")
            return [] 


    def write_to_file(self, filename: str, content: str) -> str:
        file_path = self.get_file_path(filename)
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(str(content))
        return str(file_path)


    def read_from_file(self, filename: str) -> str:
        file_path = self.get_file_path(filename)
        with open(file_path, "r") as file:
            print(file_path)
            return file.read()

    def file_exists(self, filename: str) -> bool:
        return self.get_file_path(filename).exists()


    def read_given_line(self, filename, line):
        file_path = self.get_file_path(filename)
        with open(file_path, "r", encoding="utf-8") as file:
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
        with open(file_path, 'r', encoding="utf-8") as file:
            lines = file.readlines()

        lines[line] = str(value) + '\n'

        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(lines)


    def matrix_csv(self, path):
        main = []
        file_path = self.get_file_path(path)
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                if "id," not in line:                
                    main.append(line.split(','))
        return main

    def rl_csv(self, path, id):
        file_path = self.get_file_path(path)
        with open(file_path, 'r', encoding="utf-8") as file:
            for line in file:
                if id in line:
                    return line.split(',')[id]

    def del_content(self, path):
        file_path = self.get_file_path(path)
        open(file_path, 'w').close()

    def app_csv(self, path, value):
        file_path = self.get_file_path(path)
        with open(file_path, 'a', newline='', encoding="utf-8") as fileTemp:  
            csvwriter = csv.writer(fileTemp)
            csvwriter.writerow(value)

    def uniq_id(self):
        return ''.join(random.choice(self.char) for _ in range(10))

    def search_line_csv(self, path, value):
        file_path = self.get_file_path(path)
        try:
            with open(file_path, mode='r', encoding='utf-8') as file_csv:
                csv_file = csv.reader(file_csv)
                for i, lines in enumerate(csv_file):
                    if len(lines) > 0 and lines[0] == value[0] or value in lines: 
                        #horrible mais peut fonctionner
                        return i
                return -1 
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error reading file: {file_path}") from e

    def delete_row_csv(self, path, line_number):
        file_path = self.get_file_path(path)
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
                reader = list(csv.reader(infile))

                if line_number < 1 or line_number > len(reader):
                    raise IndexError(f"line_number {line_number} is out of bounds for the file with {len(reader)} rows.")
                rows_to_keep = reader[:line_number - 1] + reader[line_number:]

            with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(rows_to_keep)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error processing file: {file_path}") from e

    def replace_csv_row(self, path, line_number, new_row):
        file_path = self.get_file_path(path)
        try:
            with open(file_path, mode='r', newline='', encoding='utf-8') as infile:
                reader = list(csv.reader(infile))

                if line_number < 1 or line_number > len(reader):
                    raise IndexError(f"line_number {line_number} is out of bounds for the file with {len(reader)} rows.")
                
                reader[line_number - 1] = new_row

            with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
                writer = csv.writer(outfile)
                writer.writerows(reader)

        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")
        except Exception as e:
            raise RuntimeError(f"Error processing file: {file_path}") from e

