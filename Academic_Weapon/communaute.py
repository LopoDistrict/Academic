import flet as ft
from typing import Union
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
        self.page_height = 500

    def send_data(self, e, target_page):
        time.sleep(0.1)
        e.scale = 2
        e.page.go(target_page)

    def upload_document(self, path):
        ftp_server = ftplib.FTP("ftpupload.net", "if0_37857418", "DjZERKKLUQIgSbl")
        ftp_server.encoding = "utf-8"

        with open(path, "wb") as file:
            ftp_server.retrbinary(f"RETR {path}", file.write)

        ftp_server.dir()

        with open(path, "r") as file:
            print("File Content:", file.read())

        ftp_server.quit()

    def retrieve_data_server(self, e) -> tuple:
        # [0] title, [1] description, [2] size, [3] date, [4] size, [5] type
        mydb = mysql.connector.connect(
            user="if0_37857418",
            password="DjZERKKLUQIgSbl",
            host="sql200.infinityfree.com",
            database="if0_37857418_aw",
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

            self.index += 1
            nv_label = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(value_retrived[0], size=18, weight=ft.FontWeight.BOLD),
                                ft.Text(value_retrived[1], size=15),
                                ft.Text(
                                    f"{value_retrived[2]} • {value_retrived[5]}",
                                    size=12,
                                    color="#d2dbe3",
                                ),
                                ft.Text(f"Par {value_retrived[5]}", size=11, color="#5af979"),
                            ]
                        ),
                        ft.Icon(name=self.extension_file.get(".pdf", ft.icons.FILE), size=60),
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
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.TextField(
                    label="Chercher des documents...",
                    on_change=lambda e: print("Search:", e.control.value),
                ),
                ft.Text(
                    "Document récents de la communauté",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Divider(height=5, color="white"),
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
