import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
import time
import datetime
import math
from tool_fold import file_manager


def send_data(e, target_page):
    time.sleep(0.1)
    e.page.go(target_page)


def accueil(router_data: Union[Router, str, None] = None):
    # Determine greeting based on current hour
    x = datetime.datetime.now()
    hour = int(x.strftime("%H"))
    if 8 <= hour <= 12:
        value_hour = "Bonjour"
    elif hour >= 18:
        value_hour = "Bonsoir"
    else:
        value_hour = "Bon Après midi, "

    fs = file_manager.FileSystem()

    # Main content
    content = ft.Container(
        ft.Column(
            [
                ft.Text(value_hour, size=30, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Work Streak", size=25, weight=ft.FontWeight.BOLD),
                            ft.Icon(name=ft.icons.LOCAL_FIRE_DEPARTMENT),
                            ft.Text("5"),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        
                    ),
                    height=60,
                    bgcolor="#3870a4",
                    padding=ft.padding.only(left=10),
                ),
                ft.Divider(height=1, color="white"),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Heure travaillé: "+str(int(fs.read_given_line("assets/user_data/user_log.txt", 0))/60)[0:4] + " min.", 
                            size=17, weight=ft.FontWeight.BOLD), #a mettre le read d'un fichier
                            
                            ft.OutlinedButton(
                                icon=ft.icons.ACCESS_TIME,
                                text="Continuer à travailler",
                                on_click=lambda e: send_data(e, "/pomodoro"),
                                height=50,
                                style=ft.ButtonStyle(                                    
                                    shape=ft.RoundedRectangleBorder(radius=20),
                                    bgcolor="#3870a4",
                                    overlay_color="#1d5384",
                                ),
                            ),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    height=60,
                ),

                ft.Divider(height=1, color="white"),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Dernier Document Travaillé ", size=17, weight=ft.FontWeight.BOLD), #a mettre le read d'un fichier
                            ft.FilledButton(
                                icon=ft.icons.INSERT_DRIVE_FILE,
                                text=f"{fs.get_last_modified()}", 
                                width=60,
                                height=40,                            
                                on_click=lambda e: send_data(e, "/librairie"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    color="#FFFFFF",
                                    bgcolor="#3B556D",  
                                    overlay_color="#5FC2BA",
                                ),
                            ),
                        ],
                        
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    height=50,
                ),
            ],
            spacing=65,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        height=700,
        padding=ft.padding.all(10),
        border_radius=20,
    )

    return content
