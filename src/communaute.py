import flet as ft
from typing import Union
import os.path
import logging


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class sql_data:
    def __init__(self):
        self.index = 1
        self.extension_file = {
            ".pdf": ft.icons.PICTURE_AS_PDF,
            ".jpg.jpeg.png.webp": ft.icons.IMAGE,
            ".docx.txt.doc.odt": ft.icons.FOLDER_COPY_ROUNDED,
        }
        self.is_named_search = True
        self.page_height = 400
        self.like_icon = ft.Icon(name=ft.icons.FAVORITE, color="#dcdcdc", size=40)
        self.char = (
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
        )
        self.temp_file_id = ""

        self.title_aff = ft.Text(size=23, weight=ft.FontWeight.BOLD)
        self.info_aff = ft.Text(size=15)
        self.type_aff = ft.Text(size=15)
        self.desc_aff = ft.Text(size=14, color="#ababab")
        self.download = ""
        self.id = ""
        self.UI_object = UI()


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
                        ft.Row(
                            [
                                ft.FilledButton(
                                    icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                                    text="Telecharger",
                                    on_click=lambda e: (
                                        self.handle_download(e, self.download)
                                    ),
                                    height=50,
                                    icon_color="#FFFFFF",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=15),
                                        color="#FFFFFF",
                                        bgcolor="#4b5059",
                                    ),
                                    animate_scale=ft.Animation(
                                        duration=300,
                                        curve=ft.AnimationCurve.EASE_IN_OUT,
                                    ),
                                ),
                                ft.FilledButton(
                                    icon=ft.Icons.FAVORITE_BORDER,
                                    text="Liker",
                                    on_click=lambda e: (
                                        self.save_like(
                                            e,
                                            self.id,
                                            self.title_aff.value,
                                            self.desc_aff.value,
                                            self.download,
                                        ),
                                    ),
                                    height=50,
                                    icon_color="#FFFFFF",
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=15),
                                        color="#FFFFFF",
                                        bgcolor="#de0a0a",
                                    ),
                                    animate_scale=ft.Animation(
                                        duration=300,
                                        curve=ft.AnimationCurve.EASE_IN_OUT,
                                    ),
                                ),
                            ]
                        ),
                    ],
                    height=300,
                    spacing=20,
                ),
            ),
        )

    def get_id_from_subject(self, subject):
        sub = {"Maths": 1,
            "Biologie": 2,
            "Informatique": 3,
            "Littérature": 4,
            "Anglais": 5,
            "Langues Internationales": 6,
            "Histoire/Geographie": 7,
            "Geopolitique": 8,
            "Philosophie": 9,
            "Economie": 10,
            "Physique/Chimie": 11,
            "Art": 12,
            "Droit": 13,
            "Ingénieurie": 14,
            "Médecine": 15,
            "Autre": 16,}

        return sub[subject]

    def handle_download(self, e, url):
        from random import randint
        from tool_fold import file_manager

        fs = file_manager.FileSystem()
        ret = fs.download(url)
        if ret == -1:
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Une erreur est survenue lors du téléchargement")
            )
            e.page.snack_bar.open = True
            e.page.update()
        else:
            file_path = "assets/user_data/user_log.txt"
            old_xp = int(fs.read_given_line(file_path, 3))
            fs.append_file(str(randint(3, 15) + old_xp), 3, file_path)

            e.page.snack_bar = ft.SnackBar(ft.Text("le fichier a été téléchargé"))
            e.page.snack_bar.open = True
            e.page.update()

    def show(self, e, title, desc, type, info, url, id_v):
        self.title_aff.value = title
        self.info_aff.value = (
            str(int(info.split("_")[0]) / 10**6) + " MB " + info.split("_")[1]
        )
        self.type_aff.value = "type de fichier: ." + type
        self.desc_aff.value = desc
        self.download = url
        self.id = id_v

        logging.info(f"title_aff.value {self.title_aff.value}")
        logging.info(f"info_aff.value  {self.info_aff.value}")
        logging.info(f"type_aff.value  {self.type_aff.value}")
        logging.info(f"desc_aff.value  {self.desc_aff.value}")

        e.page.open(self.info)

    def uniq_id(self):
        from random import choice
        return "".join(choice(self.char) for _ in range(10))

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
        titles = {
            "/feed": 0,
            "/outil": 1,
            "/pomodoro": 1,
            "/": 2,
            "/about": 2,
            "/communaute": 3,
            "/librairie": 4,
        }
        e.page.navigation_bar.selected_index = titles[target_page]
        e.page.go(target_page)
        e.page.update()

    def upload_document_db(self, title, description, file_name, subject_type, ):
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
                    mycursor.execute(
                        "SELECT num_document FROM document ORDER BY num_document DESC LIMIT 1;"
                    )
                    myresult = mycursor.fetchone()
                    last_num_document = myresult[0] if myresult else 0
                    new_num_document = last_num_document + 1

                    sql = """
                    INSERT INTO document (id_document, nom_document, description_document, taille_document, date_document, id_user, num_document, extension_file, id_type)
                    VALUES (%s, %s, %s, %s, SYSDATE(), %s, %s, %s, %s)
                    """
                    user_id = "test_user"
                    self.temp_file_id = self.uniq_id()

                    logging.info(f"File size: {os.path.getsize(file_name)}")
                    values = (
                        self.temp_file_id,
                        title,
                        description,
                        os.path.getsize(file_name),
                        user_id,
                        new_num_document,
                        file_name.split(".")[-1],
                        self.get_id_from_subject(subject_type)
                    )
                    mycursor.execute(sql, values)
                    mydb.commit()
                    logging.info("Document data inserted successfully.")
        except Error as err:
            logging.error(f"Database error: {err}")
            raise
        except Exception as ex:
            logging.error(f"Unexpected error in upload_document_db: {ex}")
            raise

    def handle_search(self, e, value, etiquette_data, load, bool_search_name):
        etiquette_data.controls.clear()
        e.page.update()
        search_results = self.search(value, bool_search_name)
        if search_results:
            logging.info(f"Value searched {search_results}")
            logging.info(f"bool_search_name {bool_search_name}")
            self.add_new_label(e, search_results, etiquette_data, load, True)
        else:
            logging.info("No search results found.")
            etiquette_data.controls.append(ft.Text("Aucun résultat trouvé."))
            e.page.update()





    def search(self, value, bool_search_name):
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

                    if bool_search_name:
                        sql = "SELECT * FROM document WHERE nom_document LIKE %s LIMIT 10"
                        mycursor.execute(sql, (f"%{value}%",))
                    else:
                        subject_id = self.get_id_from_subject(value)
                        print(f"subject_id {subject_id}")
                        sql = "SELECT * FROM document WHERE id_type = %s LIMIT 15"
                        mycursor.execute(sql, (subject_id,))
                    result = mycursor.fetchall()
                    return result
        except Error as err:
            logging.error(f"Database error: {err}")
            return ()
        except Exception as ex:
            logging.error(f"Unexpected error in search: {ex}")
            return ()




    def retrieve_data_server(self) -> tuple:
        import mysql.connector

        try:
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
            mydb.close()
            mycursor.close()
            return myresult

        except Error as err:
            logging.error(f"Database error: {err}")
            return ()
        except Exception as ex:
            logging.error(f"Unexpected error in retrieve_data_server: {ex}")
            return ()
        finally:
            mydb.close()
            mycursor.close()



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

                ftp_server.cwd("htdocs")
                ftp_server.cwd("com_docs")

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
            try:
                if like_icon.color == "#dcdcdc":
                    like_icon.color = "#db025e"
                    fs.app_csv("assets/user_data/liked.csv", [id, nom, desc, lien])
                    try:
                        page.snack_bar = ft.SnackBar(
                            ft.Text(
                                "ce document a été sauvegardé - retrouvé le dans la librarie"
                            )
                        )
                        page.snack_bar.open = True
                        e.page.update()
                    except:
                        pass
                else:
                    like_icon.color = "#dcdcdc"
                    ligne = fs.search_line_csv("assets/user_data/liked.csv", lien)
                    fs.delete_row_csv("assets/user_data/liked.csv", ligne + 1)

                e.page.update()

            except:
                fs.app_csv("assets/user_data/liked.csv", [id, nom, desc, lien])
                try:
                    page.snack_bar = ft.SnackBar(
                        ft.Text(
                            "ce document a été sauvegardé - retrouvé le dans la librarie"
                        )
                    )
                    page.snack_bar.open = True
                    e.page.update()
                except:
                    pass
        except Exception as ex:
            logging.error(f"Error in save_like: {ex}")




    def retrieve_normalise(self, e, etiquette_data,load):
        data = []
        for j in range(3):
            nv_data = self.retrieve_data_server()[0]
            if nv_data:
                data.append(nv_data)
                self.index += 1
            else:
                break
        self.add_new_label(e, data, etiquette_data, load, False)




    def add_new_label(self, e, data, etiquette_data, load, is_value_given):
        #séparer les fonctionnalités
        from tool_fold import file_manager
        logging.info(f"New label data: {data}")
        #load.visible = True
        self.UI_object.show_loader(e)
        try:
            fs = file_manager.FileSystem()
            i_turn = len(data) if is_value_given else 4
            for i in range(i_turn):
                try:
                    #if not is_value_given:
                        #data = []
                        #for j in range(4):
                        #    #Horrrible
                        #    #mais solution temporaire
                        #    nv_data = self.retrieve_data_server()[0]
                        #    if nv_data:
                        #        data.append(nv_data)
                        #        self.index += 1
                        #    else:
                        #        break
                        ##data = data[0]
                        #logging.info(f"Retrieve data: {data}")
                        ##Meme moi j'ai honte bordel
                    doc_id = data[i][0]
                    print("error flag1")
                    if not fs.is_present_csv("assets/user_data/liked.csv", doc_id):
                        like_icon = ft.Icon(name=ft.icons.FAVORITE, color="#dcdcdc", size=40)
                        nv_label = ft.Container(
                            content=ft.Row(
                                [
                                    ft.Column(
                                        controls=[
                                            ft.Text(data[i][1], size=18, weight=ft.FontWeight.BOLD),
                                            ft.Text(data[i][2], size=15),
                                            ft.Text(
                                                f"{data[i][3]}B • {data[i][7]}",
                                                size=12, color="#d2dbe3",
                                            ),

                                        ]
                                    ),
                                    ft.Container(
                                        content=like_icon,
                                        on_click=lambda e, title=data[i][1], desc=data[i][2], 
                                                            url=f"https://academic-weapon.rf.gd/com_docs/{doc_id}.{data[i][7]}", 
                                                            id=doc_id: self.save_like(e, id, title, desc, url),
                                        scale=ft.transform.Scale(scale=1),
                                        animate_scale=ft.animation.Animation(800, ft.AnimationCurve.BOUNCE_OUT),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            padding=15,
                            border_radius=7,
                            on_click=lambda e, url_link=f"https://academic-weapon.rf.gd/com_docs/{doc_id}.{data[i][7]}",
                                            titre=data[i][1], desc=data[i][2], type_d=data[i][7], 
                                            info=f"{data[i][3]}_{data[i][5]}", id_d=doc_id: 
                                            self.show(e, titre, desc, type_d, info, url_link, id_d),
                            scale=ft.transform.Scale(scale=0),
                            animate_scale=ft.animation.Animation(800, ft.AnimationCurve.BOUNCE_OUT),
                        )
                        etiquette_data.controls.append(nv_label)
                        etiquette_data.controls.append(ft.Divider(height=10, color="white", thickness=3))
                        nv_label.scale = 1
                        e.page.update()
                        logging.info(
                            f"Click show {data[i][1], data[i][2], data[i][7], data[i][3] + '_' + data[i][5]}"
                        )                   
                    #else:
                    #    i_turn += 1
                    
                except Exception as ex1:
                    logging.error(f"An error occurred (probably out of range) in add_new_label: {ex1}")
                    break

            if len(data) < 3:
                etiquette_data.controls.append(
                    ft.Text("Il n'y a plus de documents disponibles. Revenez plus tard."))
                logging.info("No more data to retrieve.")
                return

        except Exception as ex:
            logging.error(f"An error occurred in add_new_label: {ex}")
        finally:
            #load.visible = False
            self.UI_object.hide_loader(e)
            e.page.update()


class UI:
    #Juste pour ne pas mettre le loader et snackbar dans une classe random
    def __init__(self):
        self.loader_alert = ft.AlertDialog(
            content=ft.Row(
                [
                    ft.Text("Chargement", weight=ft.FontWeight.BOLD),
                    ft.ProgressRing(width=36, height=36, stroke_width=5)
                ]
            )
        )

    def show_loader(self, e):
        e.page.open(self.loader_alert)
        e.page.update()  # Update the dialog

    def hide_loader(self, e):
        e.page.close(self.loader_alert)
        self.pageloader_alert.update()  # Close and update the dialog


class login_form:
    #-----------------
    #TODO 
    # fait- faire les snackbar en cas d'erreur
    #fait- remove la clé à chaque lancement d'app si l'utilisateur n'a pas spécifié is_remember
    #loading visibility 
    #search prévoir cas ou l'user cherche plusieurs que 10 
    #mettre les scnack bar dans une fonction de class UI
    #On ne peut pas afficher le nom de l'utilisateur => faille de securité
    #possible
    #-------------------------

    def __init__(self, obj_sql_data):
        self.is_login = False #il l'appelle en vrai et affiche le login 
        # puis le transforme en faux (create account)
        self.id_user = ""
        self.obj_sql_data = obj_sql_data
        self.user_is_logged_on = False
        self.user_name = ""

    def check_encryption_token(self):
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
                    from tool_fold import file_manager
                    fs = file_manager.FileSystem()
                    file_path = fs.get_file_path('assets/user_data/.enc')
                    with open(file_path) as f:
                        hash_token = f.readline()
                        hash_token = hash_token


                    logging.info("INFO - file has been read")
                    sql = """SELECT id_user FROM user WHERE %s = SHA2(CONCAT(id_user, nom_user, mdp_user), 256)"""
                    mycursor.execute(sql, (hash_token, ))
                    result = mycursor.fetchall()
                    logging.info("INFO - value has been retrieved")
                    if not result:
                        return False

                    self.user_is_logged_on = True
                    return True

        except Error as err:
            logging.error(f"Database error: {err}")
            raise
        except Exception as ex:
            logging.error(f"error while checking the encryption key: {ex}")
            raise

    def write_encryption_token(self, name, psswd):
        from tool_fold import file_manager
        fs = file_manager.FileSystem()
        enc_file_path = fs.get_file_path("assets/user_data/.enc")
        with open(enc_file_path, "w") as file_enc:
            hash_value = (
                        self.encrypt_SHA256(self.id_user)  
                        + self.encrypt_SHA256(name) 
                        + self.encrypt_SHA256(psswd)
                    )

            file_enc.write(hash_value)

    def encrypt_SHA256(self, hash_string):
        logging.info(f"raw data {hash_string}")
        import hashlib
        sha_signature = \
            hashlib.sha256(hash_string.encode()).hexdigest()
        return sha_signature

    def handle_login(self, e, name, psswd, confirm=None, email=None, is_remember=None):
        self.is_login = not self.is_login
        logging.info(f"self.is_login {self.is_login}")

        if self.is_login == False:
            if psswd == confirm and confirm is not None:
                return_value_creating_account = self.create_account(name, psswd, confirm, email)
                if return_value_creating_account:
                    e.page.snack_bar = ft.SnackBar(
                        ft.Text("Le compte a été créée avec succès")
                    )
                    e.page.snack_bar.open = True
                    e.page.update()
                    logging.info(f"INFO - Sucess creating account")

                else:
                    logging.info(f"ERROR - Failed creating account")

                    e.page.snack_bar = ft.SnackBar(
                        ft.Text("Une erreur est survenu tentez plus tard ")
                    )
                    e.page.snack_bar.open = True
                    e.page.update()
            else:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text("Les mots de passes sont différents")
                )

                e.page.snack_bar.open = True
                e.page.update()
                print("pas le même mdp")
        else:
            self.id_user = self.signup(name, psswd)[0][0] # [()]
            if not self.id_user:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text("Mauvais identifiant ou mot de passe")
                )
                e.page.snack_bar.open = True
                e.page.update()
                logging.info("Error: wrong credentials")
                logging.info(f"self.id_user {self.id_user}")
            
            #elif is_remember:
            else:
                if is_remember:
                    from tool_fold import file_manager
                    fs = file_manager.FileSystem()
                    fs.append_file(False, 8, "assets/user_data/.enc")

                e.page.snack_bar = ft.SnackBar(
                ft.Text("Vous êtes maintenant connecté en tant que: {name} ")
                )
                e.page.snack_bar.open = True
                e.page.update()
                self.user_name = name
                logging.info(f"INFO - Sucess login in")
                self.write_encryption_token(name, psswd)



    def signup(self, name, psswd):
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
                    sql = """SELECT id_user FROM user WHERE nom_user = %s AND mdp_user = %s"""
                    mycursor.execute(sql, (self.encrypt_SHA256(name), self.encrypt_SHA256(psswd)))
                    result = mycursor.fetchall()
                    return result

        except Error as err:
            logging.error(f"Database error: {err}")
            raise
        except Exception as ex:
            logging.error(f"Unexpected error in signup: {ex}")
            raise

    def create_account(self, name, psswd, confirm, email):
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
                    if not self.is_login:
                        sql = """INSERT INTO user (id_user, nom_user, mdp_user, email_user) 
                        VALUES (%s, %s, %s, %s)"""
                        #on encrypt les valeurs après les tests pour éviter 
                        #de laisser en raw dans la base de données les informations utilisateurs
                        values = (                            
                            self.encrypt_SHA256(self.obj_sql_data.uniq_id()),
                            self.encrypt_SHA256(name),
                            self.encrypt_SHA256(psswd),
                            self.encrypt_SHA256(email)
                        )
                        mycursor.execute(sql, values)
                        mydb.commit()
                        return True
        except Error as err:
            logging.error(f"Database error: {err}")
            return False
        except Exception as ex:
            logging.error(f"Unexpected error in upload_document_db: {ex}")
            return False


            
                    
def communaute(router_data: Union[str, None] = None):
    etiquette = sql_data()
    user_login_object = login_form(etiquette)
    selected_file = {}
    ui_object = UI()
    

    def loading_encryption_handling():  
        #ui_object.show_loader(e)
        if user_login_object.check_encryption_token():
            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Connecté en tant que: {user_login_object.user_name}")
            )
            e.page.snack_bar.open = True
            e.page.update()

        #ui_object.hide_loader(e)

    def add_file_pick(e):
        try:
            logging.info("Starting file picker")
            pick_files_dialog.pick_files()
        except Exception as ex:
            logging.error(f"Error in add_file_pick: {ex}")

    def on_file_pick_result(e: ft.FilePickerResultEvent):
        try:
            if e.files and e.files[0].path:
                selected_file["path"] = os.path.abspath(e.files[0].path)
                selected_file["name"] = e.files[0].name
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

        if "path" not in selected_file or not os.path.exists(selected_file["path"]):
            logging.error("No file selected or file path is invalid!")
            e.page.snack_bar = ft.SnackBar(
                ft.Text("Aucun fichier sélectionné ou chemin de fichier invalide")
            )
            e.page.snack_bar.open = True
            e.page.update()
            return

        try:
            ui_object.show_loader(e)
            e.page.splash = ft.ProgressBar()
            e.page.update()
            

            etiquette.upload_document_db(
                titre.value, description.value, selected_file["path"], matiere.value
            )
            logging.info("File data uploaded to database.")

            etiquette.upload_document_ftp(selected_file["path"], selected_file["name"])
            logging.info("File uploaded to FTP server.")
            

            e.page.close(upload_alert)
            e.page.snack_bar = ft.SnackBar(ft.Text("Le fichier a bien été uploadé"))
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
            ui_object.hide_loader(e)
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




    def change_search_option(e):
        if search_option_button.text == "Rechercher par nom":
            search_option_button.text = "Rechercher par matieres"
            etiquette.is_named_search = False
            search.on_tap = handle_tap
            search.controls = [
                ft.ListTile(title=ft.Text(f"{i}"), on_click=close_anchor, data=i)
                for i in liste_matiere
            ]
        else:
            search_option_button.text = "Rechercher par nom"
            etiquette.is_named_search = True
            search.on_tap = None
            search.controls = None
        e.page.update()
        print(etiquette.is_named_search)



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
        hint_text="Entrez le sujet",
        options=[
            ft.dropdown.Option("Maths"),
            ft.dropdown.Option("Biologie"),
            ft.dropdown.Option("Informatique"),
            ft.dropdown.Option("Littérature"),
            ft.dropdown.Option("Anglais"),
            ft.dropdown.Option("Langues Internationales"),
            ft.dropdown.Option("Histoire/Geographie"),
            ft.dropdown.Option("Geopolitique"),
            ft.dropdown.Option("Philosophie"),
            ft.dropdown.Option("Economie"),
            ft.dropdown.Option("Physique/Chimie"),
            ft.dropdown.Option("Art"),
            ft.dropdown.Option("Droit"),
            ft.dropdown.Option("Ingénieurie"),
            ft.dropdown.Option("Médecine"),
            ft.dropdown.Option("Autre"),
        ],
    )

    file_pick_button = ft.FilledButton(
        text="Choisir un fichier à upload",
        icon=ft.Icons.ATTACH_FILE,
        width=225,
        height=50,
        icon_color="#FFFFFF",
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

    def handle_tap(e):
        print(f"handle_tap")
        search.open_view()
        
    def close_anchor(e):
        text = f"{e.control.data}"
        print(f"closing view from {text}")
        search.close_view(text)

    liste_matiere = ("Maths",
            "Biologie",
            "Informatique",
            "Littérature",
            "Anglais",
            "Langues Internationales",
            "Histoire/Geographie",
            "Geopolitique",
            "Philosophie",
            "Economie",
            "Physique/Chimie",
            "Art",
            "Droit",
            "Ingénieurie",
            "Médecine",
            "Autre")

    search = ft.SearchBar(
        view_elevation=2,
        divider_color=ft.Colors.AMBER,
        bar_hint_text="Chercher des documents...",
        on_change=lambda e: print("Search:", e.control.value),
        width=280,

    )

    # Connetion form
    # elements
    


    def handle_form_type(e, is_login_local):
        try: 
            user_login_object.is_login = is_login_local
            e.page.open(formulaire_login)
            content_login.controls = [] 
            content_login.controls.extend([base_content_form])

            if user_login_object.user_is_logged_on:
                content_login.controls.extend([already_connected])
                formulaire_login.value = "Connexion"
            if user_login_object.is_login:
                content_login.controls.extend(
                    [login_name, login_password, login_remember, login_button]
                )
                formulaire_login.value = "Inscription"
            else:
                content_login.controls.extend(
                    [signup_name, signup_psswd, signup_confirm_psswd, signup_email, signup_button]
                )
                
            #user_login_object.is_login = not user_login_object.is_login
            e.page.update()
        except Exception as ex:
            print(ex)

        
    already_connected = ft.Text(f"Vous êtes déja connecté en tant que: {user_login_object.user_name}")
    login_name = ft.TextField(
        label="Nom",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre nom",
    )

    login_password = ft.TextField(
        label="Mot de passe",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre mot de passe",
        password=True,  
    )

    login_remember = ft.Checkbox(label="Se souvenir de moi", value=False)

    signup_name = ft.TextField(
        label="Nom",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre nom",
    )

    signup_psswd = ft.TextField(
        label="Mot de passe",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Créez un mot de passe",
        password=True, 
    )

    signup_confirm_psswd = ft.TextField(
        label="Confirmez le mot de passe",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Confirmez votre mot de passe",
        password=True, 
    )

    signup_email = ft.TextField(
        label="Email",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre email",
    )

    login_button = ft.OutlinedButton(
        text="Se connecter",
        icon=ft.icons.ADD,
        on_click=lambda e: user_login_object.handle_login(e, login_name.value, login_password.value, login_remember.value),
        height=45,
        icon_color="#FFFFFF",
        width=200,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            overlay_color="#0080ff",
            shape=ft.RoundedRectangleBorder(radius=7),
            
        ),
    )

    signup_button = ft.OutlinedButton(
        text="S'incrire",
        icon=ft.icons.ADD,
        on_click=lambda e: user_login_object.handle_login(e, signup_name.value, signup_psswd.value,
        signup_confirm_psswd.value, signup_email.value),
        height=45,
        icon_color="#FFFFFF",
        width=200,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            overlay_color="#0080ff",
            shape=ft.RoundedRectangleBorder(radius=7),
            
        ),
    )

    base_content_form = ft.Column([
        ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        icon_color="#FFFFFF",
                        icon_size=20,
                        on_click=lambda e: e.page.close(formulaire_login),
                    )
                ],
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),

            #ft.Tabs(
            #    selected_index=1,
            #    tabs=[
            #        ft.Tab(
            #            content=ft.Container(
            #                content=ft.Text("Se connecter"), alignment=ft.alignment.center,
            #                on_click=lambda e: handle_form_type(e),
            #            )
            #        ),
            #        ft.Tab(
            #            content=ft.Container(
            #                content=ft.Text("Creer un compte+++"), alignment=ft.alignment.center,
            #                on_click=lambda e: handle_form_type(e),
            #            )
            #        )
            #    ]
            #)
    ])

    content_login = ft.Column(
        [
            
        ],
        height=350,
    )

    formulaire_login = ft.AlertDialog(
        modal=True,
        title=ft.Text("Connexion"),
        content=content_login,
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
                        ),
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
                        icon_color="#FFFFFF",
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor="#48dc03", color="#FFFFFF", overlay_color="#55ec04"
                        ),
                    ),
                    ft.FilledButton(
                        text="Annuler",
                        icon=ft.icons.CANCEL,
                        on_click=handle_close,
                        width=125,
                        icon_color="#FFFFFF",
                        height=45,
                        style=ft.ButtonStyle(
                            bgcolor="#dd050f", color="#FFFFFF", overlay_color="#ee030d"
                        ),
                    ),
                ],
            ),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )


    search_option_button = ft.FilledButton(
        icon=ft.Icons.MANAGE_SEARCH,
        text="Rechercher par nom",
        width=200,
        height=40,
        icon_color="#FFFFFF",
        on_click=lambda e:  change_search_option(e),
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
            color="#FFFFFF",
            bgcolor="#194975",
            overlay_color="#0b70d4",
        ),
        animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
    )
    etiquette_data = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )
    titre_intro = ft.Text("Bienvenue dans le Hub", size=18, weight=ft.FontWeight.BOLD)
    intro = ft.Text(
            "Retrouvez ici des documents posté par différents étudiants, Vous pouvez aussi vous même en postez dans "
        )
    
    load = ft.ProgressRing(width=36, height=36, stroke_width=5, visible=False)
    text_button = "Commencez à chercher"

    def pre_add(e, etiquette_t, etiquette_data, load, val): #val = is_value_giver
        text_button = "Chargez plus de contenu"
        titre_intro.value = ""
        intro.value = ""
        #etiquette.add_new_label(e, etiquette_t, etiquette_data, load, val)
        etiquette.retrieve_normalise(e, etiquette_data, load)

    def check_if_user_login_before_upload(e):
        if not user_login_object.user_is_logged_on:
            if user_login_object.check_encryption_token(): #on recheck
                #quand meme au cas il se serait login entre temps
                setup_file_picker(e.page)
                e.page.open(upload_alert)                
            else:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text("Avant de pouvoir upload vous devez vous connectez ou vous s'incrire")
                )
                e.page.snack_bar.open = True
                e.page.update()
        else:
            setup_file_picker(e.page)
            e.page.open(upload_alert)

    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Column(
                    [ft.Row(
                        [
                            ui_object.loader_alert,
                            ft.TextButton(
                                "Se Login",
                                icon=ft.Icons.VPN_KEY,
                                icon_color="#FFFFFF",
                                on_click=lambda e: handle_form_type(e, True),
                            ),
                            ft.TextButton(
                                "Se connecter",
                                icon=ft.Icons.PERSON_ROUNDED,
                                icon_color="#FFFFFF",
                                on_click=lambda e: handle_form_type(e, False),
                            )
                        ],
                    ),
                    ft.Row(
                        controls=[                        
                            search,
                            
                            ft.IconButton(
                                icon=ft.Icons.SEARCH,
                                icon_color="#FFFFFF",
                                icon_size=20,
                                on_click=lambda e: etiquette.handle_search(
                                    e, search.value, etiquette_data, load, etiquette.is_named_search
                                ),
                            ),
                        ],
                    ),
                    ],
                    spacing=15,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            search_option_button,
                            ft.FloatingActionButton(
                                icon=ft.icons.ADD,
                                height=50,
                                width=50,
                                on_click=lambda e: 
                                    check_if_user_login_before_upload(e)                                
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        
                    ),
                ),
                etiquette_data,
                ft.ResponsiveRow(
                    controls=[
                        titre_intro,
                        intro,
                        ft.Row(
                            controls=[
                                load,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        ft.FilledButton(
                            text=f"{text_button}",
                            on_click=lambda e: (pre_add(e, etiquette, etiquette_data, load, False)),
                            width=220,
                            height=45,
                            style=ft.ButtonStyle(
                                bgcolor="#0080ff",
                                color="#FFFFFF",
                                overlay_color="#adb4ff",
                                shape=ft.RoundedRectangleBorder(radius=2),
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=25,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=etiquette.page_height + 500,
    )
    return content
    loading_encryption_handling()
