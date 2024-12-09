import flet as ft
from . import file_manager
from random import choice 

def flash_cards(router):
    def add_new_card(e):

        def get_random_hex_color():
            return '#' + ''.join([choice('0123456789ABCDEF') for _ in range(6)])

        def flip_card(t):
            stack = card.content  # Access the Stack inside the Container
            stack.controls[0].visible = not stack.controls[0].visible
            stack.controls[1].visible = not stack.controls[1].visible
            stack.update()

        # Create the card container with flip functionality
        card = ft.Container(
            content=ft.Stack(
                [
                    ft.Container(
                        ft.Text(question.value, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=get_random_hex_color(),
                        expand=True,
                        visible=True,  # Initially the question is visible
                    ),
                    ft.Container(
                        ft.Text(response.value, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=get_random_hex_color(),
                        expand=True,
                        visible=False,  # Initially the response is hidden
                    ),
                ],
            ),
            width=300,
            height=200,
            bgcolor=get_random_hex_color(), #mettre un color picker
            border_radius=10,
            on_click=flip_card,
            padding=10,
        )
        cards_column.controls.append(card)
        e.page.close(dlg_modal)
        e.page.update()



    def handle_close(e):
        e.page.open = False
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

    # Dialog for adding a new card
    dlg_modal = ft.AlertDialog(
        modal=True,
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
    add_button = ft.FilledButton(
        text="Ajouter",
        icon=ft.icons.ADD,
        on_click=lambda e: e.page.open(dlg_modal),
        style=ft.ButtonStyle(bgcolor="#3B556D", color="#FFFFFF"),
    )



    # Column to hold the cards
    cards_column = ft.Column(
        spacing=10,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # Main layout
    col = ft.Column(
        controls=[
            ft.Row(
                [add_button],
                spacing=10,
            ),
            ft.Divider(height=5, color="white"),
            cards_column,
        ],
        spacing=15,
        expand=True,
    )
    return col
