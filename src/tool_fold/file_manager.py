import os
from pathlib import Path
import os.path, time
import datetime
import random
import ftplib
import csv


class FileSystem:
    def __init__(self):
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
        # Check if running on Android or iOS
        if self.is_android():
            storage_dir = os.getenv("EXTERNAL_STORAGE")
        elif self.is_ios():
            storage_dir = os.path.expanduser("~")
        else:
            storage_dir = os.getenv("EXTERNAL_STORAGE") or os.getenv("HOME")

        if storage_dir is None:
            storage_dir = ""
        return Path(storage_dir)

    def get_file_path(self, filename: str) -> Path:
        if self.is_android() or self.is_ios():
            return self.base_path / filename
        else:
            print(f"base path {self.base_path / ('src/' + filename)}")
            return self.base_path / ("src/" + filename)

    def is_android(self) -> bool:
        return "ANDROID_BOOTLOGO" in os.environ

    def is_ios(self) -> bool:
        return os.environ.get('RUNNING_ON_IOS', 'False') == 'True'

    def get_random_hex_color(self):
            from random import choice
            return '#' + ''.join([choice('0123456789ABCDEF') for _ in range(6)])

    def download(self, url):
        # Fill Required Information
        HOSTNAME = "ftpupload.net"
        USERNAME = "if0_37999130"
        PASSWORD = "KTihAaTOhwN"
        
        try:    
            ftp_server = ftplib.FTP(HOSTNAME, USERNAME, PASSWORD)
            ftp_server.encoding = "utf-8"            
            
            filename = url.split("/")[-1]
            filename = filename.replace("\n", "") 
            
            ftp_server.cwd('htdocs')
            ftp_server.cwd('com_docs')
            
            if("ANDROID_BOOTLOGO" in os.environ): 
                download_dir = "/storage/emulated/0/Download"

            elif (os.environ.get('RUNNING_ON_IOS', 'False') == 'True'):                
                download_dir = os.path.expanduser('~/Documents')
                download_dir = os.path.join(documents_path, 'Downloads')
        
                if not os.path.exists(download_dir):
                    os.makedirs(download_dir)

            local_file_path = os.path.join(download_dir, filename)
                        
            os.makedirs(download_dir, exist_ok=True)
            
            with open(local_file_path, "wb") as file:
                ftp_server.retrbinary(f"RETR {filename}", file.write)
            
            print(f"File downloaded successfully: {local_file_path}")
            
        except ftplib.all_errors as e:
            print(f"FTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if 'ftp_server' in locals():
                ftp_server.quit()

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


    def read_given_line(self, filename, line): #return la valeur ini
        file_path = self.get_file_path(filename)
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()[line].split("=")[1]

    def read_given_line_ini_name(self, filename, line):
        file_path = self.get_file_path(filename)
        with open(file_path, "r", encoding="utf-8") as file:
            return file.readlines()[line].split("=")[0]

    def get_last_modified(self):
        doc_path = self.get_file_path("document/")
  
        if len(os.listdir(doc_path)) == 0: 
            # si le dossier est de base vide on a pas a check 
            return None
        else:
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

        lines[line] = self.read_given_line_ini_name(path, line) + "=" + str(value) + '\n'

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

    def is_present_csv(self, file, value):
        file_path = self.get_file_path(file)
        with open(file_path, mode='r', encoding='utf-8') as f:
            file_csv = csv.reader(f)
            for line in file_csv:
                if value == line[0]:
                    print(f"TRUE {line[0]} == {value}")
                    return True
        return False

    def add_xp(self,value):
        try:
            file_path = self.get_file_path("assets/user_data/user_log.txt")
            old_xp = int(self.read_given_line(file_path, 3))
            self.append_file(str(value + old_xp), 3, file_path)

        except:
            print("error while recup xp")

    def read_matrix_json(self, path):
        import json
        l = []
        file_path = self.get_file_path(path)
        with open(file_path) as json_file:
            json_data = json.load(json_file)
        
        for item in json_data:
            for data_item in item['calendar']:
                l.append((data_item["titre"],data_item["desc"],data_item["date"]))
        return l

    def add_json_list(self, path, new_event):
        import json
        try:
            json_file_path = self.get_file_path(path)
            with open(json_file_path, "r") as file:
                data = json.load(file)
            
            # Append the new event to the "calendar" list
            data[0]["calendar"].append(new_event)
            
            with open(json_file_path, "w") as file:
                json.dump(data, file, indent=4)
            
            print("Event added successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")