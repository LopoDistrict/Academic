import flet as ft
from typing import Union
import random  # Import missing module
import time
import os.path
import mysql.connector
import ftplib


class sql_data:
    def __init__(self):
        self.index = 0
        self.extension_file = {
            ".pdf": ft.icons.PICTURE_AS_PDF,
            ".jpg.jpeg.png.webp": ft.icons.IMAGE,
            ".docx.txt.doc.odt": ft.icons.FOLDER_COPY_ROUNDED,
        }
        self.page_height = 1000

        self.char = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        )

    def uniq_id(self):
        return ''.join(random.choice(self.char) for _ in range(10))

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        print("___start pick_files_result")
        if e.files:
            file_names = ", ".join(f.name for f in e.files)
            print(f"Files selected: {file_names}")
        else:
            print("File selection cancelled.")

    
    def send_data(self, e, target_page):
        time.sleep(0.1)
        e.scale = 2
        e.page.go(target_page)


    def upload_document_db(self, e, info_file):
        mydb = mysql.connector.connect(
            user="academic_togetherme",
            password="5279abd1804fbed3cd683f591a5b51001acc32f2",
            host="72con.h.filess.io",
            database="academic_togetherme",
            port=3306,
        )

        mycursor = mydb.cursor()
        mycursor.execute("SELECT TOP 1 num_document FROM document ORDER BY num_document DESC ")
        myresult = mycursor.fetchall()

        mycursor.execute(
            #pour l'instant dans isèuser on met null le temps de finir l'authentificator
            f"INSERT INTO document VALUES({uniq_id}, {e.title.value}, {e.description.value}, {info_file}, SYSDATE, NULL, {myresult[0]})"
        )
        
        mycursor.close()
        mydb.close()
        

    #mettre des try et except

    def upload_document_ftp(self, path):
        ftp_server = ftplib.FTP("ftpupload.net", "if0_37857418", "DjZERKKLUQIgSbl")
        ftp_server.encoding = "utf-8"

        with open(path, "wb") as file:
            ftp_server.retrbinary(f"RETR {path}", file.write)
         #taille
        ftp_server.dir()
        with open(path, "r") as file:
            print("File Content:", file.read())

        ftp_server.quit()
        upload_document_db(os.path.getsize(path))


    def retrieve_data_server(self, e) -> tuple:
        # [0] title, [1] description, [2] size, [3] date, [4] size, [5] type
        mydb = mysql.connector.connect(
            user="academic_togetherme",
            password="5279abd1804fbed3cd683f591a5b51001acc32f2",
            host="72con.h.filess.io",
            database="academic_togetherme",
            port=3306,
        )

        mycursor = mydb.cursor()
        mycursor.execute(
            f"SELECT * FROM document WHERE num_document = {self.index} ORDER BY date_document ASC"
        )
        myresult = mycursor.fetchall()
        mycursor.close()
        mydb.close()
        return myresult
        
    

    def add_new_label(self, e):  # -> void
        for i in range(5):
            value_retrived = self.retrieve_data_server(e)
            if not value_retrived:
                print("No more data to retrieve.")
                return
            taille = 0 #faire le calcul pour la taille

            self.index += 1
            nv_label = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(value_retrived[1], size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(value_retrived[2], size=15),
                                ft.Text(
                                    f"{taille} • {value_retrived[1].split('.')[-1]}",
                                    size=12,
                                    color="#d2dbe3",
                                ),
                                ft.Text(f"Par {value_retrived[5]}", size=11, color="#5af979"),
                            ]
                        ),
                        ft.Icon(name=self.extension_file.get(value_retrived[1].split('.')[-1]), size=60),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=15,
                bgcolor="#3B556D",
                border_radius=7,
                on_click=lambda e: print("Clickable without Ink clicked!"),
            )
            e.page.add(nv_label)

def communaute(router_data: Union[str, None] = None):
    etiquette = sql_data()
    selected_file = {}  # Dictionary to store file information

    def add_file_pick(e):
        print("___start add_file_pick")
        pick_files_dialog.pick_files()

    def on_file_pick_result(e: ft.FilePickerResultEvent):
        print("___start pick_files_result")
        if e.files:
            selected_file['path'] = e.files[0].path  # Store the file path
            selected_file['name'] = e.files[0].name  # Store the file name
            print(f"File selected: {selected_file['name']}")
        else:
            print("File selection cancelled.")

    def handle_upload(e):
        # Check if a file has been selected
        if 'path' not in selected_file:
            print("No file selected!")
            return

        # Upload the file to the FTP server
        try:
            etiquette.upload_document_ftp(selected_file['path'])
            print("File uploaded to FTP server.")

            # Save metadata to the database
            etiquette.upload_document_db(e, selected_file['name'])
            print("File data uploaded to database.")
        except Exception as ex:
            print(f"Error during upload: {ex}")

    # Initialize the file picker
    pick_files_dialog = ft.FilePicker(on_result=on_file_pick_result)

    # Add the file picker dialog to the page overlay
    def setup_file_picker(page):
        if pick_files_dialog not in page.overlay:
            page.overlay.append(pick_files_dialog)

    # Page content
    titre = ft.TextField(
        label="Titre",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez un titre",
    )
    description = ft.TextField(
        label="Description (courte)",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez une courte description",
        multiline=True,
        max_lines=4,
    )
    matiere = ft.Dropdown(
        width=225,
        hint_text="Entrez le sujet ou la matière",
        options=[
            ft.dropdown.Option("Maths"),
            ft.dropdown.Option("Biologie"),
            ft.dropdown.Option("Informatique"),
            ft.dropdown.Option("Littérature"),
            ft.dropdown.Option("Anglais"),
            ft.dropdown.Option("Langues Internationales"),
            ft.dropdown.Option("Histoires/Geographie"),
            ft.dropdown.Option("Geopolitique"),
            ft.dropdown.Option("Philosophie"),
            ft.dropdown.Option("Economie"),
            ft.dropdown.Option("Physique/Chimie"),
            ft.dropdown.Option("Art"),
            ft.dropdown.Option("Droit"),
            ft.dropdown.Option("Ingénieurie"),
            ft.dropdown.Option("Médecine"),
            ft.dropdown.Option("Divers"),
            ft.dropdown.Option("Autre"),
        ],
    )

    file_pick_button = ft.FilledButton(
        text="Choisir un fichier à upload",
        icon=ft.icons.FILE_PRESENT,
        width=225,
        height=50,
        on_click=add_file_pick,  # Attach the correct function
        style=ft.ButtonStyle(
            bgcolor="#1582ee",
            color="#FFFFFF",
            overlay_color="#2d8ff0",
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
    )

    tos = ft.Radio(value="Accept", label="Cet Upload Respecte les C.U")

    def handle_close(e):
        e.page.close(upload_alert)

    # Define the alert dialog
    upload_alert = ft.AlertDialog(
        modal=True,
        title=ft.Text("Upload"),
        content=ft.Container(
            ft.Column(
                [
                    titre,
                    description,
                    matiere,
                    file_pick_button,
                    tos,
                ],
                spacing=15,
            )
        ),
        actions=[
            ft.ResponsiveRow(
                [
                    ft.FilledButton(
                        text="Upload",
                        icon=ft.icons.CLOUD_UPLOAD,
                        on_click=handle_upload,  # Trigger the upload
                        width=125,
                        height=45,
                        style=ft.ButtonStyle(bgcolor="#48dc03", color="#FFFFFF", overlay_color="#55ec04"),
                    ),
                    ft.FilledButton(
                        text="Annuler",
                        icon=ft.icons.CANCEL,
                        on_click=handle_close,
                        width=125,
                        height=45,
                        style=ft.ButtonStyle(bgcolor="#dd050f", color="#FFFFFF", overlay_color="#ee030d"),
                    ),
                ],
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    # Define the page content
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    "Document récents de la communauté",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=5, color="white"),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                height=50,
                                width=50,
                                on_click=lambda e: (setup_file_picker(e.page), e.page.open(upload_alert)),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                    ),
                    padding=15,
                ),
                ft.Row(
                    controls=[
                        ft.FilledButton(
                            text="Chargez plus de contenu",
                            on_click=lambda e: etiquette.add_new_label(e),
                            width=220,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="#0080ff",
                                overlay_color="#adb4ff",
                                shape=ft.RoundedRectangleBorder(radius=2),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=35,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=etiquette.page_height,
    )

    return content
