import flet as ft
import threading
import time
from . import file_manager
import math
from random import randint

def pomodoro(router):
    fs = file_manager.FileSystem()
    old_xp = fs.read_given_line('assets/user_data/user_log.txt', 3)
    fs.append_file(randint(8,13), 3, 'assets/user_data/user_log.txt') #on lui ajoute de l'xp

    class Pomodoro(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.time_left = ft.Text(value="25:00", size=40, color="white")

            self.start_button = ft.OutlinedButton(
                text="Débuter",
                on_click=self.start_timer,
                adaptive=True,
                width=150,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    
                    color="#FFFFFF",
                    overlay_color="#0b70d4", 
                ),
            )

            self.reset_button = ft.OutlinedButton(
                text="Reset",
                on_click=self.reset_timer,
                adaptive=True,
                width=150,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    color="#FFFFFF",
                    overlay_color="#0b70d4", 
                ),
            )

            self.timer_duration = 25  # Default timer duration in minutes
            self.running = False
            self.time_remaining = self.timer_duration * 60  # Time remaining in seconds

        def build(self):
            # Build the layout
            return ft.Column(
                [
                    ft.Column(
                        [],
                        spacing=55,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Travail",
                                            size=30,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.FilledButton(
                                            text="25 min.",
                                            on_click=lambda _: self.set_timer(25),
                                            adaptive=True,
                                            width=125,
                                            height=45,
                                            style=ft.ButtonStyle(bgcolor="#939cfc", overlay_color="#adb4ff"),
                                        ),
                                        ft.FilledButton(
                                            text="50 min.",
                                            on_click=lambda _: self.set_timer(50),
                                            adaptive=True,
                                            width=125,
                                            height=45,
                                            style=ft.ButtonStyle(bgcolor="#939cfc", overlay_color="#adb4ff"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=5,
                                    width=170,
                                ),
                                bgcolor="#ab0101",
                                width=150,
                                border_radius=15,
                                padding=15,
                            ),
                            ft.Container(
                                ft.Column(
                                    [
                                        ft.Text(
                                            "Pause",
                                            size=30,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.FilledButton(
                                            text="5 min.",
                                            on_click=lambda _: self.set_timer(5),
                                            adaptive=True,
                                            width=125,
                                            height=45,
                                            style=ft.ButtonStyle(bgcolor="#939cfc", overlay_color="#adb4ff"),
                                        ),
                                        ft.FilledButton(
                                            text="15 min.",
                                            on_click=lambda _: self.set_timer(15),
                                            adaptive=True,
                                            width=125,
                                            height=45,
                                            style=ft.ButtonStyle(bgcolor="#939cfc", overlay_color="#adb4ff"),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=5,
                                    width=170,
                                ),
                                bgcolor="#25a9b2",
                                width=150,
                                border_radius=15,
                                padding=15,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [self.start_button, self.reset_button],
                        alignment=ft.MainAxisAlignment.CENTER,
                        height=115,
                    ),
                    ft.Row(
                        [self.time_left],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ]
            )

        def set_timer(self, minutes):
            self.start_button.text = "Débuter"
            if self.running:
                self.running = False  
            self.timer_duration = minutes
            self.time_remaining = self.timer_duration * 60
            self.time_left.value = f"{minutes:02}:00"
            self.update()

        def start_timer(self, e):
            if not self.running:
                self.running = True
                self.start_button.text = "Pause"
                self.update()
                self.run_timer()
            else:
                temps_tavail = (self.timer_duration * 60) - (int(self.time_left.value[3:5]) + (int(self.time_left.value[0:2])*60))
                self.write_time(str(temps_tavail))
                self.running = False
                self.start_button.text = "Continuer"
                self.update()
        
        def write_time(self, value):   
            fs = file_manager.FileSystem()
            file_path = "./assets/user_data/user_log.txt"  
            anc_val = int(fs.read_given_line("assets/user_data/user_log.txt", 0))       
            fs.append_file(str(int(value) + int(anc_val)), 0, file_path)
                

        def run_timer(self):
            def countdown():
                while self.time_remaining > 0 and self.running:
                    mins, secs = divmod(self.time_remaining, 60)
                    self.time_left.value = f"{mins:02}:{secs:02}"
                    self.update()
                    time.sleep(1)
                    self.time_remaining -= 1

                if self.running:
                    self.time_left.value = "00:00"
                    self.running = False
                    self.start_button.text = "Débuter"
                    self.update()

            thread = threading.Thread(target=countdown, daemon=True)
            thread.start()

        def reset_timer(self, e):
            self.running = False
            temps_tavail = (self.timer_duration * 60) - (int(self.time_left.value[3:5]) + (int(self.time_left.value[0:2])*60))
            self.write_time(str(temps_tavail))
            self.time_remaining = self.timer_duration * 60
            self.time_left.value = f"{self.timer_duration:02}:00"
            self.start_button.text = "Débuter"
            self.update()

    
    return Pomodoro()
