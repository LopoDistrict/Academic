import flet as ft
from . import file_manager
from random import choice, randint
import csv

def flash_cards(router):
    def load_flash_cards():
        """Load flash cards from the CSV file and display them."""
        fs = file_manager.FileSystem()
        try:
            saved = fs.matrix_csv("assets/user_data/flash_card.csv")
            for i in range(len(saved)):
                create_card(saved[i][1], saved[i][2], saved[i][0], False)
        except FileNotFoundError:
            pass

    def save_flash_card_to_csv(card_id, question_text, response_text):
        fs = file_manager.FileSystem()
        fs.app_csv("assets/user_data/flash_card.csv", [card_id, question_text, response_text])

    def delete_flash_card_from_csv(card_id):
        fs = file_manager.FileSystem()
        data = fs.read_csv("assets/user_data/flash_card.csv")
        data = [row for row in data if row[0] != card_id]  # Filter out the card to delete
        fs.del_content("assets/user_data/flash_card.csv")  # Clear the file
        for row in data:
            fs.app_csv("assets/user_data/flash_card.csv", row)  # Rewrite the remaining cards

    def create_card(question_text, response_text, card_id=None, save_to_csv=True):
        """Create a new flash card and add it to the page."""
        def get_random_hex_color():
            return '#' + ''.join([choice('0123456789ABCDEF') for _ in range(6)])

        couleur_fond = get_random_hex_color()

        def flip_card(t):
            stack = card.content
            stack.controls[0].visible = not stack.controls[0].visible
            stack.controls[1].visible = not stack.controls[1].visible
            stack.update()

        def delete_card(e):
            delete_flash_card_from_csv(card_id)  # Delete the card from the CSV file
            cards_column.controls.remove(card)  # Remove the card from the UI
            e.page.update()

        card_id = card_id or file_manager.FileSystem().uniq_id()
        print(f"card_id: {card_id}")
        card = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        ft.Text(question_text, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=couleur_fond,
                        expand=True,
                        visible=True,
                    ),
                    ft.Container(
                        ft.Text(response_text, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=couleur_fond,
                        expand=True,
                        visible=False,
                    ),
                    ft.IconButton(
                        icon=ft.icons.DELETE,
                        on_click=delete_card,
                        icon_color="#FFFFFF",
                        top=5,
                        right=5,
                    ),
                ],
            ),
            bgcolor=couleur_fond,
            width=500,
            height=200,
            border_radius=10,
            on_click=flip_card,
            padding=15,
        )

        cards_column.controls.append(card)
        if save_to_csv:
            save_flash_card_to_csv(card_id, question_text, response_text)

    def add_new_card(e):
        fs = file_manager.FileSystem()
        fs.append_file(randint(8, 13), 3, 'assets/user_data/user_log.txt')  # Add XP
        create_card(question.value, response.value, save_to_csv=True)
        response.value = ""
        question.value = ""
        e.page.close(dlg_modal)
        e.page.update()

    def handle_close(e):
        e.page.close(dlg_modal)
        e.page.update()

    # Text fields for question and response
    question = ft.TextField(
        label="Question",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre question",
        multiline=True,
        max_lines=4,
    )

    response = ft.TextField(
        label="Réponse",
        border=ft.InputBorder.UNDERLINE,
        filled=True,
        hint_text="Entrez votre réponse",
        multiline=True,
        max_lines=4,
    )

    dlg_modal = ft.AlertDialog(
        title=ft.Text("Nouvelle Carte"),
        content=ft.Column(
            [
                question,
                response,
            ],
            spacing=10,
        ),
        actions=[
            ft.Row(
                [
                    ft.TextButton("OK", on_click=add_new_card),
                    ft.TextButton("Annuler", on_click=handle_close),
                ],
                alignment=ft.MainAxisAlignment.END,
            )
        ],
    )

    # Add and save buttons
    add_button = ft.OutlinedButton(
        text="Ajouter une carte",
        icon=ft.icons.ADD,
        on_click=lambda e: e.page.open(dlg_modal),
        height=45,
        width=200,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            overlay_color="#0080ff",
            shape=ft.RoundedRectangleBorder(radius=7),
        ),
    )

    # Column to hold the cards
    cards_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # Load existing flashcards from CSV
    load_flash_cards()

    # Main layout
    col = ft.Column(
        controls=[
            ft.Row(
                [add_button],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=5, color="white"),
            cards_column,
        ],
        spacing=15,
        expand=True,
    )
    return col