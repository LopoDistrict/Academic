import flet as ft
from tool_fold.routes import router



def main(page: ft.Page):
    page.theme_mode = "dark"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#00021d"
    page.theme_mode = "dark"    # dark mode
    page.adaptive = True
   

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
    page.on_route_change = router.route_change
    router.page = page
    page.add(
        router.body
    )
    page.go('/')

ft.app(target=main, assets_dir="assets")