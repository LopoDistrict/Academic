import flet as ft
from typing import Union
import flet as ft
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
import time
import os.path, time

def send_data(e, target_page):
    time.sleep(0.1)
    e.page.go(target_page)

    


def outils(router_data: Union[Router, str, None] = None):
    content = ft.Container(      
            ft.Column(            
            [
                ft.Text("Avec quoi nous travaillons aujourd'hui?", size=20, weight=ft.FontWeight.BOLD,),
                ft.ResponsiveRow(
                    controls=[
                        ft.ElevatedButton(
                            icon=ft.icons.ACCESS_TIME,
                            text="Pomodoro",
                            width=60,
                            height=80,
                            
                            on_click=lambda e: send_data(e, "/pomodoro"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                 color="#FFFFFF",
                                bgcolor="#3B556D", 
                                overlay_color="#0080ff", 

                            ),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.CHECKLIST,
                            text="Liste à faire",
                            width=60,
                            height=80,                            
                            on_click=lambda e: send_data(e, "/todo"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3B556D",  
                                overlay_color="#0080ff",
                            ),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.EDIT_NOTE,
                            text="Simple Éditeur de note",
                            width=60,
                            height=80,
                            on_click=lambda e: send_data(e, "/simple_editeur"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                 color="#FFFFFF",
                                bgcolor="#3B556D",
                                overlay_color="#0080ff", 
                                 
                            ),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.EDIT,
                            text="Markdown note Editeur",
                            width=60,
                            height=80,
                            on_click=lambda e: send_data(e, "/markdown_editor"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3B556D",  
                                overlay_color="#0080ff",
                            ),
                            
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.FLIP,
                            text="Flash Cards",
                            width=60,
                            height=80,
                            on_click=lambda e: send_data(e, "/flash_cards"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3B556D",  
                                overlay_color="#0080ff",
                            ),
                            
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.MULTITRACK_AUDIO_SHARP,
                            text="Note Audio",
                            width=60,
                            height=80,
                            on_click=send_data,
                            elevation=100,                                                                
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3B556D",  
                                overlay_color="#0080ff",
                            ),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.DOCUMENT_SCANNER,
                            text="Visionneur de document",
                            width=60,
                            height=80,
                            
                            on_click=lambda e: send_data(e, "/doc"),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3B556D", 
                                overlay_color="#0080ff",                               
                            ),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.DRAW,
                            text="Notes en dessin",
                            width=60,
                            height=80,
                            on_click=send_data,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                 color="#FFFFFF",
                                bgcolor="#3B556D",
                                overlay_color="#0080ff",  
                            ),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.ACCOUNT_TREE_ROUNDED,
                            text="chat IA [à venir]",
                            width=60,
                            height=80,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                 color="#FFFFFF",
                                bgcolor="#2e4254",
                            ),
                        ),
                        
                        
                    ],
                    run_spacing={"xs": 10},
                    columns=1,
                ),
            ],
            spacing=35,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=1000,
    )
    return content


