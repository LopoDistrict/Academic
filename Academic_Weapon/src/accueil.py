import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
import time
import datetime
import math
from tool_fold import file_manager
from random import randint


def send_data(e, target_page):
    time.sleep(0.1)
    e.page.go(target_page)




def is_nv_streak():
    fs = file_manager.FileSystem()
    
    last_connection_str = fs.read_given_line("assets/user_data/user_log.txt", 2).strip()
    last_connection = datetime.datetime.strptime(last_connection_str, "%Y/%m/%d")

    actual_date = datetime.datetime.now().date()

    fs.append_file(actual_date.strftime("%Y/%m/%d"), 2, "assets/user_data/user_log.txt")
    anc = int(fs.read_given_line("assets/user_data/user_log.txt", 0).strip())

    days_diff = (actual_date - last_connection.date()).days

    
    if days_diff >= 2:
        fs.append_file("0", 0, "assets/user_data/user_log.txt")
        return "0"

    if days_diff >= 1:
        new_streak = anc + 1
        fs.append_file(str(new_streak), 0, "assets/user_data/user_log.txt")
        old_xp = fs.read_given_line('assets/user_data/user_log.txt', 3)
        
        fs.append_file(int(old_xp) + randint(9,15), 3, 'assets/user_data/user_log.txt') #on lui ajoute de l'xp
        
        return new_streak
    else:
        return anc
    
    
def accueil(router_data: Union[Router, str, None] = None):

    def get_level(e=None):
        fs = file_manager.FileSystem()
        exp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
        exp_value = (0, 15, 35, 55, 75, 100, 250, 310, 480, 560, 700, 820, 1000)
        for i in range(len(exp_value)):
            if exp >= exp_value[i]:
                if i + 1 < len(exp_value) and exp >= exp_value[i + 1]:
                    continue
                else:
                    fs.append_file(str(i + 1), 4, "assets/user_data/user_log.txt")
                    if e:
                        e.page.open(streak_bottom)
                    return i + 1

                    

    fs = file_manager.FileSystem()
    streak_bottom = ft.BottomSheet(
        dismissible=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(
                        "L'experience (ou xp) s'acquiet avec le temps et le travail, plus vous vous connectez et travaillez plus vous en gagnez.",
                        size=15,
                    ),
                    ft.ElevatedButton(
                        "Fermer", on_click=lambda e: e.page.close(streak_bottom)
                    ),
                ],
            ),
        ),
    )

    # Ensure get_level is called when the page is accessed
    get_level()

    x = datetime.datetime.now()
    hour = int(x.strftime("%H"))
    if 8 <= hour <= 12:
        value_hour = "Bonjour" 
    elif hour >= 18:
        value_hour = "Bonsoir"
    else:
        value_hour = "Bon Après midi, "

    val_temp = is_nv_streak()

    # Main content
    content = ft.Container(
        ft.Column(
            [
                ft.Text(value_hour, size=30, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Work Streak", size=25, weight=ft.FontWeight.BOLD),
                            ft.Icon(
                                name=ft.icons.LOCAL_FIRE_DEPARTMENT,
                                color="#e50000",
                                size=35,
                            ),
                            ft.Text(f"{val_temp}", size=19, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    height=60,
                    bgcolor="#0080ff",
                    padding=ft.padding.only(left=10),
                ),
                ft.Divider(height=1, color="white"),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text(
                                "Heure travaillé: "
                                + str(int(fs.read_given_line("assets/user_data/user_log.txt", 1)) / 60)[
                                    0:4
                                ]
                                + " min.",
                                size=17,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.OutlinedButton(
                                icon=ft.icons.ACCESS_TIME,
                                text="Continuer à travailler",
                                on_click=lambda e: send_data(e, "/pomodoro"),
                                height=50,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=20),
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
                            ft.Text("Dernier Document Travaillé ", size=17, weight=ft.FontWeight.BOLD),
                            ft.FilledButton(
                                text=f"{fs.get_last_modified()}",
                                icon=ft.icons.INSERT_DRIVE_FILE,                                
                                width=60,
                                height=40,
                                on_click=lambda e: send_data(e, "/librairie"),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    color="#FFFFFF",
                                    bgcolor="#3B556D",
                                    overlay_color="#0b70d4",
                                ),
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    height=50,
                ),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Xp et levels", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"Experience acquis: {str(fs.read_given_line('assets/user_data/user_log.txt', 3))}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Niveau: {str(fs.read_given_line('assets/user_data/user_log.txt', 4))}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.FilledButton(
                                text="Information à propos de l'xp",
                                on_click=lambda e: get_level(e),
                            ),
                            streak_bottom,
                        ],
                    ),
                    border_radius=15,
                    border=ft.border.all(2, ft.Colors.WHITE),
                    bgcolor="#55a7f3",
                    padding=10,
                ),
            ],
            spacing=75,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        height=900,
        padding=ft.padding.all(10),
        border_radius=20,
    )

    return content
