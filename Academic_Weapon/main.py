import flet as ft
from tool_fold.routes import router

def main(page: ft.Page):
    page.update()
    page.theme_mode = "dark"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#00021d"
    page.theme_mode = "dark"
    page.adaptive = True
   
    page.update()

    def handle_nav_change(e):
        if e.control.selected_index == 0:
            page.title = "Outils"
            page.go('/')


        page.update()


    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#0B162C",
        on_change=handle_nav_change,
        destinations=[
            ft.NavigationBarDestination(label="Outils", icon=ft.icons.EXPLORE),
            ft.NavigationBarDestination(label="Communauté", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )
    page.update()
    page.on_route_change = router.route_change
    router.page = page
    page.update()
    page.add(
        router.body,
    )
    page.update()
    page.go('/')
    page.update()

ft.app(target=main, assets_dir="assets")