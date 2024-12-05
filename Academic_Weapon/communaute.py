import flet as ft
from typing import Union
import flet as ft
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
import time
import os.path, time
#import mysql.connector

def send_data(e, target_page):
    time.sleep(0.1)
    e.scale = 2
    e.page.go(target_page)

    
def communaute(router_data: Union[Router, str, None] = None):
    page_height = 500
    content = ft.Container(      
            ft.Column(            
            [
                
                ft.SearchBar(
                    view_elevation=4,
                    divider_color=ft.Colors.AMBER,
                    bar_hint_text="Chercher des documents...",
                    #on_change=handle_change,
                    #on_submit=handle_submit,
                    #on_tap=handle_tap,
                    
                ),
                ft.Text("Document récents de la communauté", size=20, weight=ft.FontWeight.BOLD,),
                
                ft.Container(
                    ft.ResponsiveRow(
                        [                            
                            ft.Column(
                                [
                                    ft.Row(
                                        [                                            
                                            ft.Column([
                                                ft.Text("MCD", size=18, weight=ft.FontWeight.BOLD), #titre
                                                ft.Text("exo + correction camping", size=15), #titre
                                                ft.Text("15MB • 25/06/24", size=12, color="#d2dbe3"), #titre
                                                ft.Text("Par User1", size=11, color="#5af979")
                                            ]),                                    
                                            ft.Icon(name=ft.icons.PICTURE_AS_PDF, size=60),
                                        ],
                                        spacing=10, 
                                        alignment=ft.MainAxisAlignment.START,
                                    )
                                ]
                            )
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START,
                    ),   
                    padding=15,    
                    bgcolor="#3B556D",
                    border_radius=7,
                    on_click=lambda e: print("Clickable without Ink clicked!"),
                ),

                ft.Divider(height=5, color="white"),


            ],
            spacing=35,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=page_height,
    )
    return content


