import flet as ft
from typing import Union
import flet as ft
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
from huggingface_hub import InferenceClient
from random import choice as rand_pick


def send_data(e, target_page):
    time.sleep(0.1)
    e.page.go(target_page)


def feed(router_data: Union[Router, str, None] = None):
    def AI_response(e, value):
        client = InferenceClient(api_key="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")
        preset = {
            "libre": "",
            "question": "Peux tu me faires des Questions sur le sujet suivant: ", 
            "fiche": "AIde moi en faisant un résumé structuré sur: "
        }   

        messages = [
            {"role": "user", "content": f"{preset[value]} {prompt.value}"}
        ]

        stream = client.chat.completions.create(
            model="codellama/CodeLlama-34b-Instruct-hf",
            messages=messages, 
            temperature=0.5,
            max_tokens=6000,
            top_p=0.7,
            stream=True
        )

        # Initialize response_text.value as an empty string if it's None
        if response_text.value is None:
            response_text.value = ""

        # Dynamically update response_text with each chunk from the stream
        for chunk in stream:
            response_chunk = str(chunk.choices[0].delta.content)
            response_text.value += response_chunk  # Append the new chunk to the response_text value
            response_text.update()  # Refresh the UI to display the updated value
            print(response_chunk, end="")
        prompt.value = ""




    def handle_change(e):
        #e.page.add(ft.Text(f"Selected Index changed: {}"))

        choice =  e.control.selected_index
        if choice == 0:
            choice = "libre"
            prompt.label = rand_pick(libre)

        elif choice == 1:
            choice = "question"
            prompt.label = rand_pick(Questions)
        else:
            choice = "fiche"
            prompt.label = rand_pick(resume)

        print(f"choice {choice}")

    matiere = ft.Dropdown(
        width=225,
        hint_text="Entrez le sujet ou la matière",
        options=[
            ft.dropdown.Option("Maths"),
            ft.dropdown.Option("Biologie"),
            ft.dropdown.Option("Informatique"),
            ft.dropdown.Option("Littérature"),
            ft.dropdown.Option("Anglais"),
            ft.dropdown.Option("Langues Internationales"),
            ft.dropdown.Option("Histoires/Geographie"),
            ft.dropdown.Option("Geopolitique"),
            ft.dropdown.Option("Philosophie"),
            ft.dropdown.Option("Economie"),
            ft.dropdown.Option("Physique/Chimie"),
            ft.dropdown.Option("Art"),
            ft.dropdown.Option("Droit"),
            ft.dropdown.Option("Ingénieurie"),
            ft.dropdown.Option("Médecine"),
            ft.dropdown.Option("Divers"),
            ft.dropdown.Option("Autre"),
        ],
    )
    autre = ft.TextField(
        label="Autres Matières", expand=True, border=ft.InputBorder.UNDERLINE, max_length=20,
        border_color="#FFFFFF",border_width=2
    )
    themes = ft.TextField(
        label="Themes ex(cryptographie,méca. fluide)", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=3,
        border_color="#FFFFFF",border_width=2
    )
    explication = ft.BottomSheet(
        dismissible=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(
                        "Ces informations sont collectées pour affiner notre IA afin de pouvoir vous proposez du contenu plus adapté et intéressant",
                        size=15,
                        
                    ),
                    ft.ElevatedButton(
                        "Fermer", on_click=lambda e: e.page.close(explication)
                    ),
                ],
            ),
        ),
    )

    drawer = ft.NavigationDrawer(
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Libre",
                icon=ft.icons.BORDER_COLOR_OUTLINED,
                selected_icon=ft.Icon(ft.icons.BORDER_COLOR_ROUNDED),
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.icons.QUESTION_ANSWER_OUTLINED),
                label="Questions",
                selected_icon=ft.icons.QUESTION_ANSWER_ROUNDED,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.icons.TEXT_SNIPPET_OUTLINED),
                label="Fiches résumées",
                selected_icon=ft.icons.TEXT_SNIPPET_ROUNDED,
            ),

        ],
    )

    first_time = ft.AlertDialog(
        modal=True,
        title=ft.Text("Personnalisez votre Feed"),
        actions=[
            ft.ResponsiveRow(
                [
                    # Information section
                    ft.Column(
                        [
                            matiere,
                            ft.Text("Si autre précisez: ", size=15,weight=ft.FontWeight.BOLD),
                            autre,
                            ft.Text("Entrez vos thèmes  - séparez les par des virgules (,)", size=15,weight=ft.FontWeight.BOLD),
                            themes,
                        ],
                        spacing=20,  # Adjust spacing between information elements
                    ),
                    # Buttons section
                    ft.Row(
                        [
                            ft.FilledButton(
                                text="Confirmer",
                                icon=ft.icons.CHECK,
                                width=165,
                                height=45,
                                style=ft.ButtonStyle(bgcolor="#48dc03", color="#FFFFFF", overlay_color="#55ec04"),
                            ),
                            ft.FilledButton(
                                text=" ",
                                icon=ft.icons.QUESTION_MARK,
                                width=65,
                                height=45,
                                on_click=lambda e: e.page.open(explication),
                                style=ft.ButtonStyle(bgcolor="#009eff", color="#FFFFFF", overlay_color="#0190e8",),
                            ),
                        ],
                        spacing=10,  # Adjust spacing between buttons
                    ),
                ],
                
            ),
        ],
    )

    value = ""

    libre = ("Explique moi les matrices inversibles", "Parle moi du Droit international public", "Synthétise moi le conflit en Ukraine")
    Questions = ("cryptographie", "Droit des affaires", "Introduction au droit européen", "c++")
    resume = ("algorithme de dichotomie", "mécanique des fluides", "histologie-embryologie", "Biologie cellulaire")
    choice = "libre"

    if choice == "libre":
        value = rand_pick(libre)
    elif choice == "question":
        value = rand_pick(Questions)
    else:
        value = rand_pick(resume)

    prompt = ft.TextField(
        label=f"{value}", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=5,
        border_color="#FFFFFF",border_width=2
    )
    response_text =  ft.Text(max_lines=100)

    content = ft.Container(
        ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.ResponsiveRow(
                            [
                                ft.IconButton(
                                    icon=ft.icons.MENU,
                                    icon_color="#FFFFFF",
                                    icon_size=30,
                                    on_click=lambda e: e.page.open(drawer),
                                    tooltip="Menu IA",
                                ),
                                ft.IconButton(
                                    icon=ft.icons.SAVE_ALT,
                                    icon_color="#FFFFFF",
                                    icon_size=30,
                                    on_click=lambda e: e.page.open(drawer),
                                    tooltip="enregistrer",
                                ),
                            ],
                        ),
                    
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(
                    ft.Column(
                        [  
                            response_text,
                        ],
                        scroll=ft.ScrollMode.AUTO, 
                    ),
                    height=400,
                    padding=10,
                    border=ft.border.all(2, ft.Colors.WHITE),
                    border_radius=5,
                    bgcolor="#060606",
                ),
                ft.Column(
                    [
                        ft.Row(
                            [
                                prompt,
                                ft.OutlinedButton(
                                    icon=ft.icons.ARROW_UPWARD,
                                    height=40,
                                    width=40,
                                    style=ft.ButtonStyle(
                                        color="#FFFFFF",
                                        overlay_color="#0190e8",
                                        shape=ft.RoundedRectangleBorder(radius=7),
                                    ),
                                    on_click=lambda e: AI_response(e, choice)
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    spacing=35,
                    scroll=ft.ScrollMode.ALWAYS,
                ),
            ],
        ),
    )
    return content


