import flet as ft

def main(page: ft.Page):
    page.add(ft.Image(src=f"/icons/tools_icon.png"))

ft.app(
    main,
    assets_dir="assets"
)