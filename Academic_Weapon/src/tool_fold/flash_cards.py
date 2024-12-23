import flet as ft
from . import file_manager
from random import choice, randint
from . import file_manager

def flash_cards(router):
    def add_new_card(e):
        fs = file_manager.FileSystem()
        old_xp = fs.read_given_line('assets/user_data/user_log.txt', 3)
        fs.append_file(randint(8,13), 3, 'assets/user_data/user_log.txt') #on lui ajoute de l'xp

        fs.app_csv("assets/user_data/flash_card.csv", [fs.uniq_id(), question.value, response.value])

        def get_random_hex_color():
            return '#' + ''.join([choice('0123456789ABCDEF') for _ in range(6)])

        couleur_fond = get_random_hex_color()
        """
        if color_choice.value == "Rouge":
            couleur_fond = "#ff0000"
        elif color_choice.value == "Vert":
            couleur_fond = "#17e302"
        elif color_choice.value == "Bleu":
            couleur_fond = "#0061ff"
            """

        def flip_card(t):
            stack = card.content  
            stack.controls[0].visible = not stack.controls[0].visible
            stack.controls[1].visible = not stack.controls[1].visible
            stack.update()

        card = ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Container(
                        ft.Text(question.value, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=couleur_fond,
                        expand=True,
                        visible=True,  # Initially the question is visible
                    ),
                    ft.Container(
                        ft.Text(response.value, size=20, weight=ft.FontWeight.BOLD),
                        alignment=ft.alignment.center,
                        bgcolor=couleur_fond,
                        expand=True,
                        visible=False,  # Initially the response is hidden
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=500,
            height=200,
            bgcolor="#FFFFFF", #mettre un color picker
            border_radius=10,
            on_click=flip_card,
            padding=10,
            
        )
        response.value = ""
        question.value = ""
        cards_column.controls.append(card)
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

    color_choice = ft.Dropdown(
                        width=225,
                        hint_text="Entrez une couleur",
                        options=[
                            ft.dropdown.Option("Rouge"),
                            ft.dropdown.Option("Vert"),
                            ft.dropdown.Option("Bleu"),
                            ft.dropdown.Option("Random"),
                        ],
                    ),

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
