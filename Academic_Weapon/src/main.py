import flet as ft
from tool_fold.routes import router
from tool_fold import file_manager
import os
from random import randint, choice
import time
import logging
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def check_debbug():
    time.sleep(1)
    files = (
        "accueil.py", "communaute.py", "librairie.py", "outils.py", "State.py",
        "tool_fold/doc.py", "tool_fold/file_manager.py", "tool_fold/flash_cards.py",
        "tool_fold/markdown_editor.py", "tool_fold/note.py", "tool_fold/pomodoro.py",
        "tool_fold/Router.py", "tool_fold/routes.py", "tool_fold/simple_editeur.py",
        "tool_fold/todo.py"
    )
    fs = file_manager.FileSystem()

    for file in files:
        if not fs.file_exists(file):
            return False
    return True

async def main(page: ft.Page):
    page.update()
    page.theme_mode = "dark"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#0e0e0e"
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
        "Apprendre d'hier. Vivre pour aujourd'hui. Espérez pour demain. ~ Albert Einstein"
    ]

    ph = ft.PermissionHandler()
    page.overlay.append(ph)
    page.update()

    permission_container = ft.Column()

    async def request_permissions(e):
        try:
            manage_result = ph.request_permission(ft.PermissionType.MANAGE_EXTERNAL_STORAGE)
            storage_result = ph.request_permission(ft.PermissionType.STORAGE)

            if manage_result and storage_result:
                page.add(ft.Text(f"Requested MANAGE_EXTERNAL_STORAGE: {manage_result}"))
                page.add(ft.Text(f"Requested STORAGE: {storage_result}"))
                page.update()

                fs = file_manager.FileSystem()
                fs.read_given_line("assets/user_data/user_log.txt", 0)
                page.add(ft.Text("File read, no error"))

                page.add(ft.Text(os.getcwd()))
                page.add(ft.Text(str(os.environ)))

                for root, dirs, files in os.walk(os.getcwd()):
                    if dirs:
                        for dir_name in dirs:
                            page.add(ft.Text(f"  - {dir_name}"))
                    if files:
                        for file_name in files:
                            page.add(ft.Text(f"f  - {file_name}"))
                    else:
                        page.add(ft.Text("No file"))
            else:
                page.add(ft.Text("Failed to grant required permissions."))
        except Exception as error:
            logging.error(f"Error in request_permissions: {error}")
            page.add(ft.Text(f"Error: {error}"))

    loading_screen = ft.ResponsiveRow(
        [
            ft.Container(
                content=ft.Column(
                    [
                        ft.ResponsiveRow(
                            [
                                ft.Text(
                                    "Academic Weapon",
                                    size=28,
                                    weight=ft.FontWeight.BOLD,
                                    text_align=ft.TextAlign.CENTER
                                ),
                            ],
                        ),
                        ft.Container(height=50),
                        ft.ResponsiveRow(
                            [
                                ft.Image(
                                    src="assets/icon.png",
                                    width=80,
                                    height=270,
                                    repeat=ft.ImageRepeat.NO_REPEAT,
                                    border_radius=ft.border_radius.all(10),
                                ),
                            ],
                        ),
                        ft.Container(height=40),
                        ft.ResponsiveRow(
                            [
                                ft.Text(
                                    f"{choice(quote_list)}",
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    italic=True
                                ),
                                ft.ProgressBar(width=400, height=10, color="#0080ff", bgcolor="#eeeeee"),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=20,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                alignment=ft.alignment.center,
                padding=ft.padding.all(20),
            ),
        ],
        spacing=35,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(loading_screen)

    await asyncio.sleep(3)  # Simulate loading
    logging.info(f"Debug check: {check_debbug()}")
    loading_screen.controls.clear()
    page.update()

    def save(e):
        try:
            fs = file_manager.FileSystem()
            fs.append_file(nom.value, 5, "assets/user_data/user_log.txt")
            e.page.close(alerte_nom)
        except Exception as ex:
            logging.error(f"Error in save: {ex}")
            e.page.snack_bar = ft.SnackBar(ft.Text(f"Erreur: {ex}"))
            e.page.snack_bar.open = True
            e.page.update()

    nom = ft.TextField(label="Votre nom")

    alerte_nom = ft.AlertDialog(
        modal=True,
        content=ft.Text("Entrez votre Nom/pseudo"),
        actions=[
            ft.Column(
                [
                    nom,
                    ft.Row(
                        [
                            ft.TextButton("Continuez", on_click=save),
                        ],
                    ),
                ],
                spacing=25,
            ),
        ],
    )

    fs = file_manager.FileSystem()
    logging.info(f"Given: {fs.read_given_line('assets/user_data/user_log.txt', 5)}")
    if not len(fs.read_given_line("assets/user_data/user_log.txt", 5).strip()):
        logging.info("Nom/pseudo is empty")
        page.open(alerte_nom)
        page.update()

    def handle_nav_change(e):
        selected_index = e.control.selected_index
        titles = ["feed", "Outils", "Accueil", "Communauté", "Librairie"]
        routes = ["/feed", "/outil", "/", "/communaute", "/librairie"]

        if 0 <= selected_index < len(titles):
            page.title = titles[selected_index]
            page.go(routes[selected_index])
        page.update()

    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#0B162C",
        selected_index=2,
        on_change=handle_nav_change,
        destinations=[
            ft.NavigationBarDestination(label="Feed", icon=ft.icons.ALL_INCLUSIVE),
            ft.NavigationBarDestination(label="Outils", icon=ft.icons.EXPLORE),
            ft.NavigationBarDestination(label="Accueil", icon=ft.icons.HOME),
            ft.NavigationBarDestination(label="Commu.", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )

    page.on_route_change = router.route_change
    router.page = page

    page.add(
        router.body,
        permission_container,
    )

    page.go("/")
    page.update()

ft.app(target=main, assets_dir="assets")