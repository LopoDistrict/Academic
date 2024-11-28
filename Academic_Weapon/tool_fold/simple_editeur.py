import flet as ft
import time
import datetime

def simple_editeur(router):
    class Simple_editeur(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.t = ft.TextField(
                bgcolor="#151515", 
                height=500,
                multiline=True,
                min_lines=1,
                max_lines=200,
                border="#fff",
                border_color=ft.colors.TRANSPARENT,
                expand=True,
                label="Ecrivez vos notes ici",
                value=" "
                )
        
 
        def build(self):
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.FilledButton(text="Enreg.",icon=ft.icons.SAVE_ALT, on_click=lambda _: self.save(),
                                adaptive=True, 
                                style=ft.ButtonStyle(bgcolor="#3B556D", color="#FFFFFF"),),                        
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

        def save(self):
            with open("document/new_doc1.txt", "w") as file:
                file.write(self.t.value)
                file.close()   
    return Simple_editeur()   
