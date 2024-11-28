import flet as ft
import time
import threading

from flet_model import Model



class Pomodoro(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.time_left = ft.Text(value="25:00", size=40, color="white")

        self.start_button = ft.FilledButton(
            text="Débuter",
            on_click=self.start_timer,
            adaptive=True,
            width=150,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

        self.reset_button = ft.FilledButton(
            text="Reset",
            on_click=self.reset_timer,
            adaptive=True,
            width=150,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
        )

        self.timer_duration = 25  # Default timer duration in minutes
        self.running = False
        self.time_remaining = self.timer_duration * 60  # Time remaining in seconds

    def build(self):
        return ft.Column(
            [
                
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    


def main(page: ft.Page):
    page.title = "Pomodoro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#00021d"
    page.theme_mode = "dark"    # dark mode
    page.adaptive = True  
    # Navigation bar
    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#221d42",
        destinations=[
            ft.NavigationBarDestination(label="Outils", icon=f"/icons/tools_icon.png"),
            ft.NavigationBarDestination(label="Communauté", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )

    page.add(Pomodoro())


ft.app(target=main, assets_dir="assets")
