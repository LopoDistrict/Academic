import flet as ft
import sys 
import os.path
from typing import Union
from . import file_manager



def markdown_editor(router):
    def update_preview(e):
        """
        Updates the RHS (markdown/preview) when the content of the textfield changes.
        """
        md.value = text_field.value
        e.page.update()
    
    def handle_close(e):
        e.page.close(dlg_modal)

    def load_from_save(e: ft.FilePickerResultEvent):
        if e.files and len(e.files) > 0:  
            selected_file = (e.files[0].path).split("src")[-1]
            
            fs = file_manager.FileSystem()
            try:
                content = fs.read_from_file(selected_file)  # Read the file content
                text_field.value = content
                md.value = content

                
                e.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Fichier ouvert: {selected_file}")
                )
                e.page.snack_bar.open = True
                e.page.update()
            except Exception as ex:
                e.page.snack_bar = ft.SnackBar(
                    ft.Text(f"Erreur lors de l'ouverture du fichier: {ex}")
                )
                e.page.snack_bar.open = True
                e.page.update()
    
    def fp(e):
        pick_files_dialog.pick_files(allow_multiple=False, 
        allowed_extensions=["md", "txt", "py", "cpp", "js", ".java", ".jar"],
        initial_directory="./document")

    def save(e):
        """
        Save the content to a file.
        """
        fs = file_manager.FileSystem()
        file_path = fs.write_to_file("./document/" + nom_fic.value + ".md", text_field.value)
        
        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Fichier sauvegardé: {nom_fic.value}")
        )
        e.page.snack_bar.open = True
        e.page.update()
        e.page.close(dlg_modal)

        value = randint(0, 10)
        old_xp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
        fs.append_file(str(int(value) + int(old_xp)), 3, file_path)
        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Vous avez gagné: {value} xp")
        )
        e.page.snack_bar.open = True
        e.page.update()

    pick_files_dialog = ft.FilePicker(on_result=load_from_save)


    router.page.overlay.append(pick_files_dialog)
    router.page.update()

    nom_fic = ft.TextField(label="Nom du fichier")
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Voulez vous sauvegarder votre travail?"),
        actions=[
            ft.Column(
                [
                    nom_fic,
                    ft.Row(
                        [
                            ft.TextButton("Oui", on_click=save),
                            ft.TextButton("Non", on_click=handle_close),
                        ],
                    ),
                ],
                spacing=25,
            ),
        ],
    )

    def close_help(e):
        e.page.close(dlg_help)

    dlg_help = ft.AlertDialog(
        modal=True,
        title=ft.Text("Aide Markdown"),
        content=ft.Text("""
        _en italique_           # petit titre
        __en gras__             ## gros titre
        - une                   ### gros gros titre
        - liste
        - [x] liste              ``` ecrire du code```
        - [ ]  barré 
        ## Tables        
        | colonne 1     | colonne 2  |
        |---------------|-------------|
        |ceci est un     | tableau      |
        """),
        actions=[
            ft.Row(
                [
                    ft.TextButton("Fermer", on_click=close_help),
                ],
            ),
        ],
    )

    help_button = ft.OutlinedButton(
        text="aide",
        icon=ft.icons.HELP,
        on_click=lambda e: e.page.open(dlg_help),
        adaptive=True,
        width=100,
        height=50,
        style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
    )

    save_button = ft.OutlinedButton(
        text="Enreg.",
        icon=ft.icons.SAVE_ALT,
        on_click=lambda e: e.page.open(dlg_modal),
        adaptive=True,
        width=100,
        height=50,
        style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
    )
    load_button = ft.OutlinedButton(
        text="Charger",
        icon=ft.icons.FOLDER_COPY_ROUNDED,
        on_click=fp,
        adaptive=True,
        width=100,
        height=50,
        style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
    )

    text_field = ft.TextField(
        value="## ecrivez ici, le rendu est en bas vv",
        multiline=True,
        on_change=update_preview,
        expand=True,
        border_color=ft.colors.TRANSPARENT,
        label="Ecrivez vos notes ici",
        max_lines=9,
    )
    
    md = ft.Markdown(
        value=text_field.value,
        selectable=True,
        extension_set="gitHubWeb",
        on_tap_link=lambda e: e.page.launch_url(e.data),
    )

    col = ft.Column(
        controls=[
            ft.Row([help_button, save_button, load_button]),
            text_field,
            ft.Divider(height=5, color="white"),
            ft.Container(
                ft.Column([md], scroll="hidden"),
                expand=True,
                alignment=ft.alignment.top_left,
            ),
        ],
        spacing=15,
        expand=True,
    )
    return col
