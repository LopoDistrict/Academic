import flet as ft
import os
from . import file_manager
from random import randint
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def markdown_editor(router):
    def update_preview(e):
        """
        Updates the RHS (markdown/preview) when the content of the textfield changes.
        """
        md.value = text_field.value
        e.page.update()

    def handle_close(e):
        e.page.close(dlg_modal)

    def load_file(e, file_path):
        try:
            with open(file_path, "r") as file:
                content = file.read()

            text_field.value = content
            md.value = content

            e.page.snack_bar = ft.SnackBar(ft.Text(f"Fichier ouvert: {file_path}"))
            e.page.snack_bar.open = True
            e.page.update()

            e.page.close(dlg_modal)
        except Exception as ex:
            logging.error(f"Error loading file: {ex}")
            e.page.snack_bar = ft.SnackBar(ft.Text(f"Erreur lors de l'ouverture du fichier: {ex}"))
            e.page.snack_bar.open = True
            e.page.update()

    def get_document_directory():
        """
        Returns the path to the document directory based on the environment.
        """
        return os.path.join(os.getcwd(), "document" if "ANDROID_BOOTLOGO" in os.environ else "src/document")

    def show_file_explorer(e):
        """
        Displays a file explorer dialog to select a file.
        """
        document_dir = get_document_directory()
        file_buttons = []

        if os.path.exists(document_dir):
            for file_name in os.listdir(document_dir):
                if file_name.endswith((".md", ".txt", ".py", ".cpp", ".js", ".java", ".jar")):
                    file_button = ft.ElevatedButton(
                        text=file_name,
                        on_click=lambda e, fn=file_name: load_file(e, os.path.join(document_dir, fn)),
                        style=ft.ButtonStyle(color="#0080ff", shape=ft.RoundedRectangleBorder(radius=10)),
                    )
                    file_buttons.append(file_button)
        else:
            file_buttons.append(ft.Text("Le dossier 'document' n'existe pas."))

        file_explorer_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Sélectionnez un fichier"),
            content=ft.Column(
                file_buttons,
                scroll=ft.ScrollMode.AUTO,
                height=200,
                width=300,
            ),
            actions=[ft.TextButton("Fermer", on_click=lambda e: e.page.close(file_explorer_dialog))],
        )

        e.page.dialog = file_explorer_dialog
        file_explorer_dialog.open = True
        e.page.update()

    def save(e):
        """
        Save the content to a file.
        """
        fs = file_manager.FileSystem()
        file_path = fs.write_to_file(f"document/{nom_fic.value}.md", text_field.value)

        e.page.snack_bar = ft.SnackBar(ft.Text(f"Fichier sauvegardé: {nom_fic.value}"))
        e.page.snack_bar.open = True
        e.page.update()

        value = randint(0, 10)
        old_xp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
        fs.append_file(str(value + old_xp), 3, file_path)
        e.page.snack_bar = ft.SnackBar(ft.Text(f"Vous avez gagné: {value} xp"))
        e.page.snack_bar.open = True
        e.page.update()

    # UI Components
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
        actions=[ft.TextButton("Fermer", on_click=close_help)],
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
        on_click=show_file_explorer,
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
            ft.Container(
                content=text_field,
                expand=True,
            ),
            ft.Divider(height=5, color="white"),
            ft.Container(
                content=ft.Column([md], scroll=ft.ScrollMode.AUTO),
                expand=True,
                alignment=ft.alignment.top_left,
            ),
        ],
        spacing=15,
        expand=True,
    )
    return col