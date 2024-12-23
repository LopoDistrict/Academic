import flet as ft
from tool_fold.routes import router
from tool_fold import file_manager
import os
from random import randint, choice
import time

def check_debbug():
    time.sleep(1)
    files = ("accueil.py", "communaute.py", "librairie.py", "outils.py", "State.py",
    "tool_fold/doc.py", "tool_fold/file_manager.py", "tool_fold/flash_cards.py",
    "tool_fold/markdown_editor.py", "tool_fold/note.py", "tool_fold/pomodoro.py",
    "tool_fold/Router.py", "tool_fold/routes.py", "tool_fold/routes.py", 
    "tool_fold/simple_editeur.py", "tool_fold/todo.py")
    fs = file_manager.FileSystem()

    for i in range(len(files)):
        if (not fs.file_exists(files[i])):
            return False
    return True


def main(page: ft.Page):
    page.update()
    page.theme_mode = "dark"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#151515"
    page.adaptive = True
    page.window.width = 375
    page.padding = ft.padding.only(left=16, top=50, right=16)
    page.scroll = ft.ScrollMode.HIDDEN
    quote_list = [
        "Il est difficile d'échouer, mais il est pire de n'avoir jamais essayé de réussir ~ T.Roosevelt",
        "Votre paresse est un manque de respect pour les personnes qui croient en vous",
        "L'éducation est l'arme la plus puissante que vous puissiez utiliser pour changer le monde. ~B.B. King",
        "L'esprit n'est pas un récipient à remplir, mais un feu à allumer ~Plutarque",
        "La procrastination rend les choses faciles difficiles et les choses difficiles plus difficiles. ~Mason Cooley",
        "L'expert en quoi que ce soit a déjà été un débutant . ~Helen Hayes",
        "Apprendre d'hier. Vivre pour aujourd'hui. Espérez pour demain. ~ Albert Einstein" ]
    #page.window_full_screen = True

    
    ph = ft.PermissionHandler()
    page.overlay.append(ph)
    page.update()

    permission_container = ft.Column()

    def request_permissions(e):
        manage_result = ph.request_permission(ft.PermissionType.MANAGE_EXTERNAL_STORAGE)
        storage_result = ph.request_permission(ft.PermissionType.STORAGE)

        if manage_result and storage_result:
            #permission_container.controls.clear() 
            page.add(ft.Text(f"Requested MANAGE_EXTERNAL_STORAGE: {manage_result}"))
            page.add(ft.Text(f"Requested STORAGE: {storage_result}"))
            page.update()

            try:
                fs = file_manager.FileSystem()
                fs.read_given_line("assets/user_data/user_log.txt", 0)
                page.add(ft.Text("file read, no error"))

                page.add(ft.Text(os.getcwd()))
                page.add(ft.Text(os.environ()))

                for root, dirs, files in os.walk(os.getcwd()):
                    if dirs:                        
                        for dir_name in dirs:
                            page.add(ft.Text(f"  - {dir_name}"))
                    if files:
                        for file_name in files:
                            page.add(ft.Text(f"f  - {file_name}"))
                    else:
                        page.add(ft.Text("no file"))


            except Exception as error:
                page.add(ft.Text(error))

                page.add(ft.Text(os.getcwd()))
                page.add(ft.Text(os.environ()))

                for root, dirs, files in os.walk(os.getcwd()):
                    if dirs:                        
                        for dir_name in dirs:
                            page.add(ft.Text(f"  - {dir_name}"))
                    if files:
                        for file_name in files:
                            page.add(ft.Text(f"f  - {file_name}"))
                    else:
                        page.add(ft.Text("no file"))

        else:
            page.add(ft.Text("Failed to grant required permissions."))


    loading_screen =ft.ResponsiveRow(
        [
            ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            ft.Text("Chargement", size=25, weight=ft.FontWeight.BOLD),                
                            ft.Image(
                                src="src/assets/icon.png",
                                width=50,
                                height=50,
                                fit=ft.ImageFit.NONE,
                                repeat=ft.ImageRepeat.NO_REPEAT,
                                border_radius=ft.border_radius.all(10),
                            ),
                            ft.ProgressBar(width=400, color="#0080ff", bgcolor="#eeeeee"),
                            ft.Text(f"{choice(quote_list)}", size=15, weight=ft.FontWeight.BOLD, italic=True),
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                
            ),
            alignment=ft.alignment.center,
            padding=ft.padding.all(20),  
        ),
        ],
        spacing=35,
    )
     

    page.add(loading_screen)

    #time.sleep(3)
    print(check_debbug())
    loading_screen.controls.clear()
    page.update()

    """
    permission_container.controls.append(
        ft.Column(
            controls=[
                ft.Text(
                    "Pour fonctionner Academic Weapon a besoin d'avoir accès au stockage (pour la sauvegarde/écriture de fichier)"
                ),
                ft.OutlinedButton(
                    "Accepter l'accès au stockage",
                    on_click=request_permissions,
                ),
            ]
        )
    )"""

    def handle_nav_change(e):
        selected_index = e.control.selected_index
        titles = ["Accueil", "Outils", "Communauté", "Librairie"]
        routes = ["/", "/outil", "/communaute", "/librairie"]

        if 0 <= selected_index < len(titles):
            page.title = titles[selected_index]
            page.go(routes[selected_index])
        page.update()

    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#0B162C",
        on_change=handle_nav_change,
        destinations=[
            ft.NavigationBarDestination(label="Accueil", icon=ft.icons.HOME),
            ft.NavigationBarDestination(label="Outils", icon=ft.icons.EXPLORE),
            ft.NavigationBarDestination(label="Communauté", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )

    page.on_route_change = router.route_change
    router.page = page

    page.add(
        router.body,
        permission_container,  # Initially show the permission container
    )

    page.update()
    page.go("/")

ft.app(target=main, assets_dir="assets")
