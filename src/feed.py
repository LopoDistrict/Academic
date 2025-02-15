import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
from time import time
from random import choice as rand_pick
from tool_fold import file_manager
from huggingface_hub import InferenceClient

def feed(router_data: Union[Router, str, None] = None):
    choice = "libre"
    libre = (
        "Explique moi les matrices inversibles", "Parle moi du Droit international public",
        "Synthétise moi le conflit en Ukraine", "explique moi les Mathématiques appliquées", "Résume moi la Chimie organique",
        "Explique avec exemple l'Intelligence artificielle appliquée"
    )
    Questions = (
        "cryptographie", "Droit des affaires", "Introduction au droit européen", "c++", "Biologie moléculaire",
        "Finance d'entreprise", "Économie internationale", "Économie du développement"
    )
    resume = (
        "algorithme de dichotomie", "mécanique des fluides", "histologie-embryologie", "Biologie cellulaire", "Réseaux de neurones",
        "Économie micro", "Anthropologie", "Génétique", "Psychologie du développement"
    )
    exercice = (
        "pivot de Gauss", "droit des personnes", "Matrice de permutation", "Physique des particules", "Chimie physique",
        "Physique des plasmas", "Biologie des populations"
    )
    value = rand_pick(libre)
    interactive_reponse = ft.Markdown()
    response_text = ft.Markdown()
    study_feed = ft.Column()
    current_study_index = 0
    start_y = None
    last_call_time = time()
    min_delay = 5
    is_swiping = False
    fs = file_manager.FileSystem()

    def handle_pan_start(e: ft.DragStartEvent):
        nonlocal start_y, is_swiping
        start_y = e.local_y
        is_swiping = True

    def handle_pan_update(e: ft.DragUpdateEvent):
        nonlocal start_y, is_swiping, last_call_time
        if start_y is None or not is_swiping:
            return

        delta_y = e.local_y - start_y

        if delta_y < -50:
            current_time = time()
            if current_time - last_call_time >= min_delay:
                print("calling AI_response(e, choice)")
                print(f"last_call_time {last_call_time}")
                print(f"current_time {current_time}")
                last_call_time = current_time
                is_swiping = False

    def handle_pan_end(e: ft.DragEndEvent):
        nonlocal is_swiping, start_y
        is_swiping = False
        start_y = None

    def handle_close_qu(e):
        fs.append_file(niveaux.value, 6, "assets/user_data/user_log.txt")
        fs.append_file(themes.value.split(","), 7, "assets/user_data/user_log.txt")
        e.page.close(first_time)
        e.page.update()

    def handle_change(e):
        nonlocal choice, value
        choice = e.control.selected_index
        print("change ")
        print(prompt.label)

        if choice == 1:
            choice = "question"
            prompt.label = rand_pick(Questions)
            print(prompt.label)

        elif choice == 2:
            choice = "exercice"
            prompt.label = rand_pick(exercice)

        elif choice == 3:
            choice = "fiche"
            prompt.label = rand_pick(exercice)

#        elif choice == 4:
#            choice = "smart"
#            smart.visible = True
#            reponse.visible = False
#            prompt.label = "Entrez un sujet/matière"
#            e.page.update()

        else:
            choice = "fiche"
            prompt.label = rand_pick(resume)

        prompt.update()
        e.page.update()

    def AI_response(e, value):
        from random import randint
        nonlocal response_text
        fs.add_xp(str(randint(4,25)))
        print("AI_response")
        

        if not len(fs.read_given_line("assets/user_data/user_log.txt", 6).strip() == ""):
            e.page.open(first_time)
            print("empty")
        else:
            client = InferenceClient(api_key="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")
            preset = {
                "libre": "",
                "question": "Peux tu me faires des Questions sur le sujet suivant: ",
                "exercice": "Peut tu me donner des exercices structurés différents et pertinents pour en acquérir les connaissance sur: ",
                "fiche": "Aide moi en faisant un résumé structuré sur: ",
            }

            print("prompt " + preset[value] + prompt.value)
            print(value)
            difficulte = "de cette difficulté: " + fs.read_given_line("assets/user_data/user_log.txt", 6)

            messages = [
                {"role": "user", "content": f"En francais {preset[value]} {prompt.value} {difficulte}"}
            ]

            stream = client.chat.completions.create(
                #deepseek-ai/DeepSeek-R1-Distill-Qwen-32B
                #meta-llama/Meta-Llama-3-8B-Instruct
                model="deepseek-ai/deepseek-coder-1.3b-instruct",
                messages=messages,
                temperature=0.3,
                max_tokens=6000,
                top_p=0.7,
                stream=True
            )

            if response_text.value is None:
                response_text.value = ""

            response_text.value = ""
            response_text.update()

            for chunk in stream:
                response_chunk = str(chunk.choices[0].delta.content)
                response_text.value += response_chunk
                response_text.update()
                print(response_chunk, end="")
            prompt.value = ""

    def save(e):
        from time import sleep
        from random import randint
        file_path = fs.write_to_file("./document/" + nom_fic.value + ".md", response_text.value)

        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Fichier sauvegardé: {nom_fic.value}")
        )
        e.page.snack_bar.open = True
        e.page.close(dlg_modal)
        sleep(1)

        value = randint(0, 10)
        old_xp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
        fs.append_file(str(int(value) + int(old_xp)), 3, file_path)
        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Vous avez gagné: {value} xp")
        )
        e.page.snack_bar.open = True

    def handle_close(e):
        e.page.close(dlg_modal)

    smart = ft.Container(
        ft.GestureDetector(
            content=ft.Column(
                [interactive_reponse],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            on_pan_start=handle_pan_start,
            on_pan_update=handle_pan_update,
            on_pan_end=handle_pan_end,
        ),
        expand=True,
        visible=False,
        height=400,
        padding=10,
    )

    reponse = ft.Container(
        ft.Column([response_text], scroll=ft.ScrollMode.AUTO),
        height=400,
        padding=10,
        border_radius=5,
        expand=True,
        visible=True
    )

    niveaux = ft.Dropdown(
        width=225,
        hint_text="Entrez votre niveau",
        options=[
            ft.dropdown.Option("Débutant"),
            ft.dropdown.Option("Intermédiaire"),
            ft.dropdown.Option("Difficile"),
            ft.dropdown.Option("Très difficile"),
            ft.dropdown.Option("Très Avancé"),
            ft.dropdown.Option("Le plus compliqué"),
        ],
    )

    themes = ft.TextField(
        label="Themes ex(cryptographie,méca. fluide)", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=3,
        border_color="#FFFFFF", border_width=2
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

    first_time = ft.AlertDialog(
        modal=True,
        title=ft.Text("Personnalisez votre Feed"),
        actions=[
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            niveaux,
                            ft.Text("Entrez vos thèmes  - séparez les par des virgules (,)", size=15, weight=ft.FontWeight.BOLD),
                            themes,
                        ],
                        spacing=20,
                    ),
                    ft.Row(
                        [
                            ft.FilledButton(
                                text="Confirmer",
                                icon=ft.icons.CHECK,
                                width=165,
                                height=45,
                                on_click=handle_close_qu,
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
                        spacing=10,
                    ),
                ],
            ),
        ],
    )

    prompt = ft.TextField(
        label=f"{value}", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=5,
        border_color="#FFFFFF", border_width=2, bgcolor="#272727",
    )

    nom_fic = ft.TextField(label="Nom du fichier")

    drawer = ft.NavigationDrawer(
        on_change=handle_change,
        controls=[
            ft.Text("Chat IA"),
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
                icon=ft.Icon(ft.icons.MY_LIBRARY_BOOKS_OUTLINED),
                label="Exercices",
                selected_icon=ft.icons.MY_LIBRARY_BOOKS_ROUNDED,
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icon(ft.icons.TEXT_SNIPPET_OUTLINED),
                label="Fiches résumées",
                selected_icon=ft.icons.TEXT_SNIPPET_ROUNDED,
            ),
            ft.Text("Apprentissage personnalisé - A venir"),
            ft.NavigationDrawerDestination(
                label="Système d'apprentissage intelligent",
                icon=ft.Icons.SMART_TOY_OUTLINED,
                selected_icon=ft.Icon(ft.Icons.SMART_TOY_ROUNDED),
            ),
        ],
    )

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Voulez vous sauvegardez votre prompt?"),
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

    return ft.Container(
        ft.ResponsiveRow(
            [
                ft.Column(
                    [
                        ft.Row(
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
                                    on_click=lambda e: e.page.open(dlg_modal),
                                    tooltip="enregistrer",
                                ),
                            ],
                            spacing=10,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.START,
                ),

                reponse,
                smart,
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
                                )
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