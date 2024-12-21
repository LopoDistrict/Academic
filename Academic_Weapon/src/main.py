import flet as ft
from tool_fold.routes import router
from tool_fold import file_manager
import os

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
    )

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

ft.app(target=main, assets_dir="assets")
