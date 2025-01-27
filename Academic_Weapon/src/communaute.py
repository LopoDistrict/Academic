import flet as ft
from typing import Union

import os.path
import logging


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class sql_data:
    def __init__(self):
        self.index = 1
        self.extension_file = {
            ".pdf": ft.icons.PICTURE_AS_PDF,
            ".jpg.jpeg.png.webp": ft.icons.IMAGE,
            ".docx.txt.doc.odt": ft.icons.FOLDER_COPY_ROUNDED,
        }
        self.page_height = 1000
        self.like_icon = ft.Icon(name=ft.icons.FAVORITE, color="#dcdcdc", size=40)
        self.char = (
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
            't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
            'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9'
        )
        self.temp_file_id = ""

        self.title_aff = ft.Text(size=23, weight=ft.FontWeight.BOLD)
        self.info_aff = ft.Text(size=15)
        self.type_aff = ft.Text(size=15)
        self.desc_aff = ft.Text(size=14, color="#ababab")

        self.info = ft.AlertDialog(
            content=ft.Container(
                ft.Column(
                    [
                        ft.Row(
                            [
                                ft.IconButton(
                                    icon=ft.Icons.CLOSE,
                                    icon_color="#FFFFFF",
                                    icon_size=20,
                                    on_click=lambda e: e.page.close(self.info),
                                )
                            ],
                            vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                            ft.ResponsiveRow(
                            [
                                self.title_aff,
                                self.info_aff,
                                self.type_aff,
                                self.desc_aff,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                    ],
                    height=200,
                    spacing=20,
                ),
            ),
        )

    def show(self ,e , title, desc, type, info):
        self.title_aff.value = title
        self.info_aff.value = str(int(info.split("_")[0])/10**6) + "mb " + info.split("_")[1]
        self.type_aff.value = "type de fichier: ."+ type
        self.desc_aff.value = desc
        logging.info(f"title_aff.value {self.title_aff.value}")
        logging.info(f"info_aff.value  {self.info_aff.value}")
        logging.info(f"type_aff.value  {self.type_aff.value}")
        logging.info(f"desc_aff.value  {self.desc_aff.value}")

        e.page.open(self.info)

    def uniq_id(self):
        from random import choice
        return ''.join(choice(self.char) for _ in range(10))

    def pick_files_result(self, e: ft.FilePickerResultEvent):
        try:
            if e.files:
                file_names = ", ".join(f.name for f in e.files)
                logging.info(f"Files selected: {file_names}")
                file_path.value = file_names
                file_path.update()
            else:
                logging.info("File selection cancelled.")
        except Exception as ex:
            logging.error(f"Error in pick_files_result: {ex}")
            file_path.value = "Erreur lors de la sélection du fichier"
            file_path.update()

    def send_data(self, e, target_page):
        from time import sleep
        sleep(0.1)
        titles = {"/feed": 0, "/outil": 1, "/pomodoro": 1, "/": 2, "/about": 2, "/communaute": 3, "/librairie": 4}
        e.page.navigation_bar.selected_index = titles[target_page]
        e.page.go(target_page)
        e.page.update()

    def upload_document_db(self, title, description, file_name):
        from mysql.connector import Error, connect
        try:
            with connect(
                user="academic_togetherme",
                password="5279abd1804fbed3cd683f591a5b51001acc32f2",
                host="72con.h.filess.io",
                database="academic_togetherme",
                port=3306,
            ) as mydb:
                with mydb.cursor() as mycursor:
                    mycursor.execute("SELECT num_document FROM document ORDER BY num_document DESC LIMIT 1;")
                    myresult = mycursor.fetchone()
                    last_num_document = myresult[0] if myresult else 0
                    new_num_document = last_num_document + 1

                    sql = """
                    INSERT INTO document (id_document, nom_document, description_document, taille_document, date_document, id_user, num_document, extension_file)
                    VALUES (%s, %s, %s, %s, SYSDATE(), %s, %s, %s)
                    """
                    user_id = "test_user"
                    self.temp_file_id = self.uniq_id()

                    logging.info(f"File size: {os.path.getsize(file_name)}")
                    values = (self.temp_file_id, title, description, os.path.getsize(file_name), user_id, new_num_document, file_name.split(".")[-1])
                    mycursor.execute(sql, values)
                    mydb.commit()
                    logging.info("Document data inserted successfully.")
        except Error as err:
            logging.error(f"Database error: {err}")
            raise
        except Exception as ex:
            logging.error(f"Unexpected error in upload_document_db: {ex}")
            raise

    def handle_search(self, e, value, etiquette_data, load):

        etiquette_data.controls.clear()
        e.page.update()

        search_results = self.search(value)

        if search_results:

            logging.info(f"Value searched {search_results}")
            self.add_new_label(e, search_results, etiquette_data, load, True)
        else:
            logging.info("No search results found.")

    def search(self, value):
        from mysql.connector import Error, connect
        try:
            with connect(
                user="academic_togetherme",
                password="5279abd1804fbed3cd683f591a5b51001acc32f2",
                host="72con.h.filess.io",
                database="academic_togetherme",
                port=3306,
            ) as mydb:
                with mydb.cursor() as mycursor:
                    sql = "SELECT * FROM document WHERE nom_document LIKE %s LIMIT 10"
                    mycursor.execute(sql, (f"%{value}%",))
                    result = mycursor.fetchall()
                    return result
        except Error as err:
            logging.error(f"Database error: {err}")
            return ()
        except Exception as ex:
            logging.error(f"Unexpected error in search: {ex}")
            return ()

    def retrieve_data_server(self) -> tuple:
        from mysql.connector import Error, connect
        try:
            with connect(
                user="academic_togetherme",
                password="5279abd1804fbed3cd683f591a5b51001acc32f2",
                host="72con.h.filess.io",
                database="academic_togetherme",
                port=3306,
            ) as mydb:
                with mydb.cursor() as mycursor:
                    sql = "SELECT * FROM document ORDER BY date_document DESC LIMIT 10"
                    mycursor.execute(sql)
                    myresult = mycursor.fetchall()
                    return myresult

        except Error as err:
            logging.error(f"Database error: {err}")
            return ()
        except Exception as ex:
            logging.error(f"Unexpected error in retrieve_data_server: {ex}")
            return ()

    def upload_document_ftp(self, path, nom):
        from ftplib import all_errors, FTP
        try:
            with FTP("ftpupload.net", "if0_37999130", "KTihAaTOhwN") as ftp_server:
                ftp_server.encoding = "utf-8"
                new_filename = self.temp_file_id + "." + nom.split(".")[-1]
                new_path = os.path.join(os.path.dirname(path), new_filename)
                os.rename(path, new_path)

                logging.info(f"Original path: {path}")
                logging.info(f"New path: {new_path}")
                logging.info(f"New filename: {new_filename}")

                ftp_server.cwd('htdocs')
                ftp_server.cwd('com_docs')

                with open(new_path, "rb") as file:
                    ftp_server.storbinary(f"STOR {new_filename}", file)

                ftp_server.dir()
                logging.info("File uploaded to FTP server successfully.")
        except all_errors as e:
            logging.error(f"FTP error: {e}")
            raise
        except Exception as e:
            logging.error(f"Error during file upload: {e}")
            raise

    def save_like(self, e, id, nom, desc, lien):
        from tool_fold import file_manager
        try:
            fs = file_manager.FileSystem()
            like_icon = e.control.content

            if like_icon.color == "#dcdcdc":
                like_icon.color = "#db025e"
                fs.app_csv("assets/user_data/liked.csv", [id, nom, desc, lien])
            else:
                like_icon.color = "#dcdcdc"
                ligne = fs.search_line_csv("assets/user_data/liked.csv", lien)
                fs.delete_row_csv("assets/user_data/liked.csv", ligne + 1)

            e.page.update()
        except Exception as ex:
            logging.error(f"Error in save_like: {ex}")


    def add_new_label(self, e, data, etiquette_data, load, is_value_given):
        from tool_fold import file_manager
        logging.info(f"New label data: {data} - is given {is_value_given}")

        load.visible = True
        print(load)

        try:
            fs = file_manager.FileSystem()
            i_turn = 3
            if not fs:
                logging.error("FileSystem object could not be initialized.")
                return

            if is_value_given:
                i_turn = len(data)

            for i in range(i_turn):
                try:
                    if not is_value_given:
                        data = self.retrieve_data_server()
                        self.index += 1

                        if not data:
                            logging.info("No more data to retrieve.")
                            self.index -= 1
                            return

                    # Skip if the item is already in liked.csv
                    if fs.is_present_csv("assets/user_data/liked.csv", data[i][0]):
                        logging.info(f"Item {data[i][0]} already exists in liked.csv. Skipping.")
                        continue

                    like_icon = ft.Icon(name=ft.icons.FAVORITE, color="#dcdcdc", size=40)

                    # Create the label with bounce animation
                    nv_label = ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    controls=[
                                        ft.Text(data[i][1], size=18, weight=ft.FontWeight.BOLD),
                                        ft.Text(data[i][2], size=15),
                                        ft.Text(
                                            f"{data[i][3]}B • {data[i][7]}",
                                            size=12,
                                            color="#d2dbe3",
                                        ),
                                        ft.Text(f"Par {data[i][5]}", size=11, color="#5af979"),
                                    ]
                                ),
                                ft.Container(
                                    content=like_icon,
                                    on_click=lambda e, title=data[i][1], desc=data[i][2], url=f"https://academic-weapon.rf.gd/com_docs/{data[i][0]}.{data[i][7]}", id=data[i][0]:
                                    self.save_like(e, id, title, desc, url),
                                    scale=ft.transform.Scale(scale=1),
                                    animate_scale=ft.animation.Animation(800, ft.AnimationCurve.BOUNCE_OUT),
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        padding=15,
                        border_radius=7,
                        on_click=lambda e, i=i: self.show(e, data[i][1], data[i][2], data[i][7], data[i][3] + "_" + data[i][5]),
                        scale=ft.transform.Scale(scale=0),  # Start with scale 0 for animation
                        animate_scale=ft.animation.Animation(800, ft.AnimationCurve.BOUNCE_OUT),
                    )

                    # Add the label to the UI
                    etiquette_data.controls.append(nv_label)
                    etiquette_data.controls.append(ft.Divider(height=10, color="white", thickness=3))

                    nv_label.scale = 1
                    e.page.update()

                    logging.info(f"click show {data[i][1], data[i][2], data[i][7], data[i][3] + '_' + data[i][5]}")

                except Exception as ex1:
                    logging.error(f"An error occurred (probably out of range) in add_new_label: {ex1}")
                    break

        except Exception as ex:
            logging.error(f"An error occurred in add_new_label: {ex}")

        finally:
            load.visible = False
            e.page.update()

def communaute(router_data: Union[str, None] = None):
    etiquette = sql_data()
    selected_file = {}

    def add_file_pick(e):
        try:
            logging.info("Starting file picker")
            pick_files_dialog.pick_files()
        except Exception as ex:
            logging.error(f"Error in add_file_pick: {ex}")

    def on_file_pick_result(e: ft.FilePickerResultEvent):
        try:
            if e.files and e.files[0].path:
                selected_file['path'] = os.path.abspath(e.files[0].path)
                selected_file['name'] = e.files[0].name
                logging.info(f"File selected: {selected_file['name']}")
                logging.info(f"Path selected: {selected_file['path']}")
                file_path.value = f"fichier: {selected_file['name']}"
                file_path.update()
            else:
                logging.info("File selection cancelled.")
                selected_file.clear()
                file_path.value = "Pas de fichier sélectionné"
                file_path.update()
        except Exception as ex:
            logging.error(f"Error in on_file_pick_result: {ex}")
            selected_file.clear()
            file_path.value = "Erreur: Chemin de fichier invalide"
            file_path.update()

    def handle_upload(e):
        from traceback import print_exc
        if 'path' not in selected_file or not os.path.exists(selected_file['path']):
            logging.error("No file selected or file path is invalid!")
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Aucun fichier sélectionné ou chemin de fichier invalide")
            )
            e.page.snack_bar.open = True
            e.page.update()
            return

        try:
            e.page.splash = ft.ProgressBar()
            e.page.update()

            etiquette.upload_document_db(titre.value, description.value, selected_file['path'])
            logging.info("File data uploaded to database.")

            etiquette.upload_document_ftp(selected_file['path'], selected_file['name'])
            logging.info("File uploaded to FTP server.")

            e.page.close(upload_alert)
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Le fichier a bien été uploadé")
            )
            e.page.snack_bar.open = True
        except Exception as ex:
            logging.error(f"Error during upload: {ex}")
            print_exc()
            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Il y a eu une erreur dans l'upload, retentez plus tard: {ex}")
            )
            e.page.snack_bar.open = True
        finally:
            # Remove loading indicator
            e.page.splash = None
            e.page.update()

    pick_files_dialog = ft.FilePicker(on_result=on_file_pick_result)

    def close_and_send(e):
        e.page.close(upload_alert)
        etiquette.send_data(e, "/about")

    def setup_file_picker(page):
        try:
            if pick_files_dialog not in page.overlay:
                page.overlay.append(pick_files_dialog)
        except Exception as ex:
            logging.error(f"Error in setup_file_picker: {ex}")



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
        on_click=add_file_pick,
        style=ft.ButtonStyle(
            bgcolor="#1582ee",
            color="#FFFFFF",
            overlay_color="#2d8ff0",
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
    )
    file_path = ft.Text("Pas de fichier", weight=ft.FontWeight.BOLD)

    tos = ft.Radio(value="Accept", label="Cet Upload Respecte les C.U")

    def handle_close(e):
        try:
            e.page.close(upload_alert)
        except Exception as ex:
            logging.error(f"Error in handle_close: {ex}")

    search = ft.SearchBar(
        view_elevation=2,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Chercher des documents...",
        on_change=lambda e: print("Search:", e.control.value),
        width=280,
    )

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
                    file_path,
                    tos,
                    ft.TextButton(
                        "Consulter les C.U",
                        on_click=lambda e: close_and_send(e),
                        style=ft.ButtonStyle(
                            color="#0689ff",
                        )
                    ),
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
                        on_click=handle_upload,
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

    etiquette_data = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    load = ft.ProgressRing(width=36, height=36, stroke_width = 5, visible=False)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        search,
                        ft.IconButton(
                            icon=ft.Icons.SEARCH,
                            icon_color="#FFFFFF",
                            icon_size=20,
                            on_click=lambda e: etiquette.handle_search(e, search.value, etiquette_data, load)
                        )
                    ],
                ),
                ft.Text(
                    "Document récents de la communauté",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
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
                ft.Divider(height=10, color="white", thickness=3),
                etiquette_data,


                ft.ResponsiveRow(
                    controls=[
                        ft.Row(
                            [
                              load,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            height=100,
                        ),
                        ft.FilledButton(
                            text="Chargez plus de contenu",
                            on_click=lambda e: etiquette.add_new_label(e, etiquette, etiquette_data, load, False),
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
        height=etiquette.page_height + 400,
    )

    return content
