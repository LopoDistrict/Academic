import flet as ft
import time
import datetime


class Pomodoro(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.t = ft.TextField(
            bgcolor="#151515", 
            height=500,
            multiline=True,
            min_lines=1,
            max_lines=200,
            border="#fff"
            )
    
    def save(self):
        with open("document/new_doc1.txt", "w") as file:
            file.write(self.t.value)
            file.close()

    def save_interface(self):
        return ft.Container(
            ft.Text(value="Enregistrement de la note"),
            ft.TextField(
                max_lines=1,
                label="Nom de votre note",
            ),
            ft.FilledButton(text="Enregistrer",icon=ft.icons.SAVE_ALT, on_click=lambda _: self.save(),
                            adaptive=True, 
                            style=ft.ButtonStyle(bgcolor="#939cfc",),),
        )
        

    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.FilledButton(text="Enreg.",icon=ft.icons.SAVE_ALT, on_click=lambda _: self.save_interface(),
                            adaptive=True, 
                            style=ft.ButtonStyle(bgcolor="#939cfc",),),                        
                    ],
                    
                ),
                ft.Container(
                    ft.Container(  
                        ft.Column(
                            [
                                ft.Text(value=self.t.value),
                                self.t,
                            ],
                        ),      
                        bgcolor="#111",             

                    ),
                ),
            ],            
        )



def main(page: ft.Page):
    page.title = "Pomodoro"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.ADAPTIVE
    page.bgcolor = "#00021d"
    # Navigation bar

    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#221d42",
        destinations=[
            ft.NavigationBarDestination(label="Outils", icon=ft.icons.EXPLORE),
            ft.NavigationBarDestination(label="Communauté", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )

    page.add(Pomodoro())


ft.app(target=main)
