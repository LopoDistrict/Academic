import flet as ft
import time
import datetime
from . import file_manager

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

            self.nom_fic = ft.TextField(label="Nom du fichier")
            self.dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmation"),
                content=ft.Text("Voulez vous sauvegardez votre travail?"),
                actions=[
                    ft.Column(
                        [
                            self.nom_fic,
                        ft.Row(
                            [
                                ft.TextButton("Oui", on_click=self.save),
                                ft.TextButton("Non", on_click=self.handle_close),
                            ],                    
                        ),
                        ],
                        spacing=25,
                    ),
                    

                ],
            )
        

        def save(self, e):
            """
            with open(f"document/{nom_fic.value}.txt", "w") as file:
                file.write(text_field.value)
                file.close()  """

            fs = file_manager.FileSystem()
            file_path = fs.write_to_file("./document/"+self.nom_fic.value+".txt", self.t.value)

            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Fichier sauvegardé: {self.nom_fic.value}")
            )
            e.page.snack_bar.open = True
            e.page.update()
            e.page.close(self.dlg_modal)

            value = randint(0,10)
            old_xp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
            fs.append_file(str(int(value) + int(old_xp)), 3, file_path)
            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Vous avez gagné: {value} xp")
            )
            e.page.snack_bar.open = True
            e.page.update()

        def handle_close(self, e):
            e.page.close(self.dlg_modal)


        def build(self):
            return ft.Column(
                [
                    ft.Column(
                    [],
                    spacing=35,
                ),
                    ft.Row(
                        [

                                ft.FilledButton(
                                    text="Enregistrer",
                                    icon=ft.icons.SAVE_ALT,
                                    on_click=lambda e: e.page.open(self.dlg_modal),
                                    adaptive=True,
                                    width=145,
                                    height=30,
                                    
                                    style=ft.ButtonStyle(bgcolor="#3B556D", color="#FFFFFF"),
                                )
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

    return Simple_editeur()   
