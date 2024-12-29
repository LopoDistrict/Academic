import flet as ft
from random import randint
from . import file_manager

def simple_editeur(router):
    class SimpleEditeur(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.pick_files_dialog = ft.FilePicker(on_result=self.load_from_save)
            self.t = ft.TextField(
                bgcolor="#151515", 
                height=500,
                multiline=True,
                min_lines=1,
                max_lines=200,
                border_color=ft.colors.TRANSPARENT,
                expand=True,
                label="Écrivez vos notes ici",
                value=" "
            )

            self.nom_fic = ft.TextField(label="Nom du fichier")
            self.dlg_modal = None 

        def load_from_save(self, e: ft.FilePickerResultEvent):
            if e.files and len(e.files) > 0:
                selected_file = e.files[0].path
                
                fs = file_manager.FileSystem()
                try:
                    content = fs.read_from_file(selected_file)
                    self.t.value = content
                    self.t.update()
                    
                    e.page.snack_bar = ft.SnackBar(
                        ft.Text(f"Fichier ouvert: {selected_file}")
                    )
                    e.page.snack_bar.open = True
                except Exception as ex:
                    e.page.snack_bar = ft.SnackBar(
                        ft.Text(f"Erreur lors de l'ouverture du fichier: {ex}")
                    )
                    e.page.snack_bar.open = True

        def fp(self, e):
            self.pick_files_dialog.pick_files(
                allow_multiple=False, 
                allowed_extensions=["txt", "py", "cpp", "js", "java", "jar"]
            )

        def save(self, e):
            fs = file_manager.FileSystem()
            file_path = fs.write_to_file(f"./document/{self.nom_fic.value}.txt", self.t.value)

            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Fichier sauvegardé: {self.nom_fic.value}")
            )
            e.page.snack_bar.open = True
            self.dlg_modal.close()

            # Award XP
            value = randint(0, 10)
            old_xp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
            fs.append_file(str(value + old_xp), 3, file_path)

            e.page.snack_bar = ft.SnackBar(
                ft.Text(f"Vous avez gagné: {value} xp")
            )
            e.page.snack_bar.open = True

        def handle_close(self, e):
            self.dlg_modal.close()

        def build(self):
            router.page.overlay.append(self.pick_files_dialog)

            self.dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmation"),
                content=ft.Text("Voulez-vous sauvegarder votre travail?"),
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

            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.OutlinedButton(
                                text="Enreg.",
                                icon=ft.icons.SAVE_ALT,
                                on_click=lambda e: self.dlg_modal.open(),
                                width=100,
                                height=50,
                                style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
                            ),
                            ft.OutlinedButton(
                                text="Charger",
                                icon=ft.icons.FOLDER_COPY_ROUNDED,
                                on_click=self.fp,
                                width=100,
                                height=50,
                                style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
                            )
                        ],
                    ),
                    ft.Container(
                        self.t,
                        bgcolor="#111",             
                    ),
                ],            
            )

    return SimpleEditeur()
