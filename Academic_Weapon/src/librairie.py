import flet as ft
from typing import Union
from tool_fold.Router import Router
from tool_fold import file_manager
from pathlib import Path
import os

def send_data(e, target_page):
    e.page.go(target_page)

def librairie(router_data: Union[Router, str, None] = None):
    searched = ft.Column()

    extension_route = {"md": "/markdown_editor",
                    "txt": "/simple_editeur",
                    "pdf": "/doc"}

    def search(e):
        # Clear previous search results
        searched.controls.clear()
        
        if "ANDROID_BOOTLOGO" in os.environ:
            doc_path = os.path.join(os.getcwd(), "document")
        else:
            doc_path = os.path.join(os.getcwd(), "src/document")

        print(f"Document path: {doc_path}")
        
        for root, dirs, files in os.walk(doc_path):
            for filename in files:
                if e.data in filename and e.data != "":
                    print(f"Found {filename}")
                    # Create a button for the found file
                    temp_searched = ft.FilledButton(
                        icon=ft.icons.INSERT_DRIVE_FILE,
                        text=f"{filename}",
                        width=300,
                        height=40,
                        on_click=lambda e, fn=filename: send_data(e, extension_route.get(fn.split('.')[-1], "/librairie")),
                        style=ft.ButtonStyle(
                            shape=ft.RoundedRectangleBorder(radius=10),
                            color="#FFFFFF",
                            bgcolor="#3B556D",
                            overlay_color="#0b70d4",
                        ),
                    )
                    # Append the button to the 'searched' column
                    searched.controls.append(temp_searched)
        
        # Update the 'searched' column to reflect changes
        searched.update()



    fs = file_manager.FileSystem()
    liked_doc = fs.matrix_csv("assets/user_data/liked.csv")

    liked_buttons = []
    for doc in liked_doc:
        button = ft.FilledButton(
            icon=ft.icons.INSERT_DRIVE_FILE,
            text=doc[1],  
            width=300,
            height=40,
            on_click=lambda e, fn=doc[1]: send_data(e, extension_route.get(fn.split('.')[-1], "/librairie")),
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
                ft.SearchBar(
                    view_elevation=4,
                    divider_color=ft.Colors.AMBER,
                    bar_hint_text="Chercher dans vos documents...",
                    on_change=search,
                    on_submit=search,
                ),
                ft.Text("Vos documents", size=20, weight=ft.FontWeight.BOLD),
                searched,
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Récents", size=17, weight=ft.FontWeight.BOLD),
                            ft.FilledButton(
                                icon=ft.icons.INSERT_DRIVE_FILE,
                                text=f"{fs.get_last_modified()}",
                                width=300,
                                height=40,
                                on_click=lambda e, fn=fs.get_last_modified(): send_data(e, extension_route.get(fn.split('.')[-1], "/librairie")),
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
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text("Contenus likés", size=20,
                            weight=ft.FontWeight.BOLD),
                            ft.Column(liked_buttons, spacing=10),
                        ]
                    ),
                ),
            ],
            spacing=30,            
        ),
        height=700,
        border_radius=20,
    )

    return content
