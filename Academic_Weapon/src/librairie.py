import flet as ft
from typing import Union
from tool_fold.Router import Router
from tool_fold import file_manager




def bounce_animation(e):
    from time import sleep
    e.control.scale = 1.2
    e.control.update()

    # Wait for a short duration
    sleep(0.1)

    # Animate scaling back down
    e.control.scale = 1.0
    e.control.update()

def librairie(router_data: Union[Router, str, None] = None):
    searched = ft.Column()

    extension_route = {"md": "/markdown_editor",
                       "txt": "/simple_editeur",
                       "pdf": "/doc"}

    titre_f = ft.Text(size=18, weight=ft.FontWeight.BOLD)
    type_f = ft.Text(size=13)
    can_be_open = ft.Text(size=13, weight=ft.FontWeight.BOLD)
    
    url = ""

    button_col = ft.Row(
        controls=[
            ft.FilledButton(
                icon=ft.Icons.FILE_OPEN,
                text="Ouvrir",
                on_click=lambda e: (send_data(e, "/markdown_editor")),
                height=50,
                icon_color="#FFFFFF",
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=15),                                        
                    color="#FFFFFF",
                    bgcolor="#0080ff",
                ),
                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
            )
        ],
        spacing=10,
    )

    info = ft.AlertDialog(
        content=ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                icon_color="#FFFFFF",
                                icon_size=20,
                                on_click=lambda e: e.page.close(info),
                            )
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.ResponsiveRow(
                        [
                            titre_f,                                
                            type_f,
                            can_be_open,
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        controls=[
                                ft.FilledButton(
                                icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                                text="Télécharger",
                                on_click=lambda e: handle_download(e),
                                height=50,
                                icon_color="#FFFFFF",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=15),                                        
                                    color="#FFFFFF",
                                    bgcolor="#4b5059",
                                ),
                                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            ),
                            button_col,
                        ]
                    )

                ],
                height=300,
                spacing=20,
            ),
        ),
    )


    def send_data(e, target_page):    
        e.page.close(info)
        from time import sleep
        sleep(0.1)
        titles = {"/feed": 0, "/outil": 1, "/markdown_editor": 1, "/": 2, "/about": 2, "/communaute": 3, "/librairie": 4}
        if target_page in titles:
            e.page.navigation_bar.selected_index = titles[target_page]
        e.page.go(target_page)
        e.page.update()

    def show_info_file(e, titre, typef, url_f):
        titre_f.value = "Nom: " + titre
        type_f.value = "Type de fihcier: " + typef
        compatible_ext = ("md", "txt", "py", "cpp", "js", "java", "jar", "bash")
        print(f"url_f {url_f}")
        
        # Update the instance variable url
        nonlocal url
        url = url_f
        print(f"url {url}")

        if typef in compatible_ext:
            can_be_open.value = "Ce fichier peut être ouvert par l'editeur"
            can_be_open.color = "#5ae40b"
            button_col.visible = True
        else:
            can_be_open.value = "Ce fichier ne peut pas être ouvert par l'editeur"
            can_be_open.color = "#fa2e2e"
            button_col.visible = False

        e.page.dialog = info
        info.open = True
        e.page.update()


    def handle_download(e):
        # Use the instance variable url
        print(f"url: {url}")
        if "http" not in url:
            import os
            try:
                os.popen(f"cp ./document/{url} /storage/emulated/0/Download/{url}") #copy valid sur android
                try:
                    e.page.snack_bar = ft.SnackBar(ft.Text("le fichier a été téléchargé"))
                    e.page.snack_bar.open = True
                    e.page.update()
                except:
                    pass
            except:
                e.page.snack_bar = ft.SnackBar(ft.Text("Une erreur est survenu réesayez plsu tard"))
                e.page.snack_bar.open = True
                e.page.update()
        else:
            from random import randint
            fs = file_manager.FileSystem()
            ret = fs.download(url)
            if ret == -1:
                e.page.snack_bar = ft.SnackBar(ft.Text("Une erreur est survenue lors du téléchargement"))
                e.page.snack_bar.open = True
                e.page.update()
            else:
                file_path = "assets/user_data/user_log.txt"
                old_xp = int(fs.read_given_line(file_path, 3))
                fs.append_file(str(randint(3, 15) + old_xp), 3, file_path)

                e.page.snack_bar = ft.SnackBar(ft.Text("le fichier a été téléchargé"))
                e.page.snack_bar.open = True
                e.page.update()

    def search(e):
        import os
        # Clear previous search results
        searched.controls.clear()

        if "ANDROID_BOOTLOGO" in os.environ or os.environ.get('RUNNING_ON_IOS', 'False') == 'True':
            doc_path = os.path.join(os.getcwd(), "document")
        else:
            doc_path = os.path.join(os.getcwd(), "src/document")

        print(f"Document path: {doc_path}")

        for root, dirs, files in os.walk(doc_path):
            for filename in files:
                if e.data in filename and e.data != "":
                    print(f"Found {filename}")
                    # Create a button for the found file
                    temp_searched = ft.FilledButton(
                        icon=ft.icons.INSERT_DRIVE_FILE,
                        text=f"{filename}",
                        width=300,
                        height=40,
                        icon_color="#FFFFFF",
                        on_click=lambda e, titre=filename: (bounce_animation(e), show_info_file(e, filename, filename.split(".")[-1], filename)),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color="#FFFFFF",
                            bgcolor="#3B556D",
                            overlay_color="#0b70d4",
                        ),
                        animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                    )
                    # Append the button to the 'searched' column
                    searched.controls.append(temp_searched)

        searched.update()

    fs = file_manager.FileSystem()
    liked_doc = fs.matrix_csv("assets/user_data/liked.csv")

    liked_buttons = []
    if not liked_doc:
        liked_buttons.append(ft.Text("Vous n'avez rien liké pour le moment"))

    for doc in liked_doc:
        button = ft.Row(
            [
                ft.FilledButton(
                    icon=ft.icons.INSERT_DRIVE_FILE,
                    text=doc[1],
                    width=270,
                    icon_color="#FFFFFF",
                    height=40,
                    on_click=lambda e, fn=doc[1], url=doc[3], titre=doc[1]: (bounce_animation(e), show_info_file(e, titre, url.split(".")[-1], url)),
                    style=ft.ButtonStyle(
                        shape=ft.RoundedRectangleBorder(radius=10),
                        color="#FFFFFF",
                        bgcolor="#3B556D",
                        overlay_color="#0b70d4",
                    ),
                    animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                ),
                ft.IconButton(
                    icon=ft.Icons.FILE_DOWNLOAD_OUTLINED,
                    icon_color="#FFFFFF",
                    on_click=lambda e, url=doc[3]: (bounce_animation(e), handle_download(e, url)),
                    animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                ),
            ]
        )
        liked_buttons.append(button)

    if fs.get_last_modified() is None:
        recent_file_value = ft.Text("Aucun fichier récent")
    else:
        last_modified_file = fs.get_last_modified()  # Capture the value explicitly
        recent_file_value = ft.FilledButton(
            icon=ft.icons.INSERT_DRIVE_FILE,
            text=f"{last_modified_file}",
            width=270,
            height=40,
            icon_color="#FFFFFF",
            on_click=lambda e, fn=last_modified_file: (bounce_animation(e), show_info_file(e, fn, fn.split(".")[-1], fn)),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                color="#FFFFFF",
                bgcolor="#3B556D",
                overlay_color="#0b70d4",
            ),
            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
        )

    content = ft.Container(
        ft.Column(
            [
                info,
                ft.SearchBar(
                    view_elevation=4,
                    divider_color=ft.Colors.AMBER,
                    bar_hint_text="Chercher dans vos documents...",
                    on_change=search,
                    on_submit=search,
                ),
                ft.Text("Vos documents 📖", size=20, weight=ft.FontWeight.BOLD),
                searched,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Récents", size=17, weight=ft.FontWeight.BOLD),
                            ft.Column([recent_file_value]),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Contenus likés ", size=20, weight=ft.FontWeight.BOLD),
                            ft.Column(liked_buttons, spacing=10),
                        ]
                    ),
                ),
            ],
            spacing=30,
        ),
        height=700,
        border_radius=20,
    )

    return content