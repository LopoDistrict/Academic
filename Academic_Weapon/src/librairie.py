import flet as ft
from typing import Union
from tool_fold.Router import Router
from tool_fold import file_manager


def send_data(e, target_page):
    e.page.go(target_page)


def librairie(router_data: Union[Router, str, None] = None):
    fs = file_manager.FileSystem()
    liked_doc = fs.matrix_csv("assets/user_data/liked.csv")
    
    # Container for liked documents
    liked_buttons = []
    for doc in liked_doc:
        button = ft.FilledButton(
            icon=ft.icons.INSERT_DRIVE_FILE,
            text=doc[1],  # Assuming second column is the name
            width=200,
            height=40,
            on_click=lambda e: send_data(e, "/document/" + doc[0]),  # Assuming first column is ID
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=10),
                color="#FFFFFF",
                bgcolor="#3B556D",
                overlay_color="#0b70d4",
            ),
        )
        liked_buttons.append(button)
    
    # Main content
    content = ft.Container(
        ft.Column(
            [
                ft.Text("Vos documents", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Récents", size=17, weight=ft.FontWeight.BOLD),
                            ft.FilledButton(
                                icon=ft.icons.INSERT_DRIVE_FILE,
                                text=f"{fs.get_last_modified()}",
                                width=200,
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
                    content=ft.Column(
                        [
                            ft.Text("Contenus likés", size=20,
                            weight=ft.FontWeight.BOLD),
                            ft.Column(liked_buttons, spacing=10),
                        ]
                    ),
                    padding=10,
                ),
            ],
            spacing=20,
        ),
        width=400,
        height=900,
        padding=ft.padding.all(10),
        border_radius=20,
    )

    return content
