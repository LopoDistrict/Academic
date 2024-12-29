import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
from huggingface_hub import InferenceClient
from random import choice as rand_pick
from random import randint
from tool_fold import file_manager
from time import sleep



class AIApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.choice = "libre"
        self.libre = ("Explique moi les matrices inversibles", "Parle moi du Droit international public", "Synthétise moi le conflit en Ukraine")
        self.Questions = ("cryptographie", "Droit des affaires", "Introduction au droit européen", "c++")
        self.resume = ("algorithme de dichotomie", "mécanique des fluides", "histologie-embryologie", "Biologie cellulaire")
        self.exercice = ("pivot de Gauss", "droit des personnes", "Matrice de permutation")
        self.value = ""

        #utile pour première fois
        self.niveaux = ft.Dropdown(
            width=225,
            hint_text="Entrez le sujet ou la matière",
            options=[
                ft.dropdown.Option("Débutant"),
                ft.dropdown.Option("Intermédiaire"),
                ft.dropdown.Option("Difficile"),
                ft.dropdown.Option("Très difficile"),
                ft.dropdown.Option("Très Avancé"),
                ft.dropdown.Option("Le plus compliqué"),
            ],
        )
        
        self.themes = ft.TextField(
            label="Themes ex(cryptographie,méca. fluide)", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=3,
            border_color="#FFFFFF", border_width=2
        )
        self.first_time = ft.AlertDialog(
            modal=True,
            visible=False,
            title=ft.Text("Personnalisez votre Feed"),
            actions=[
                ft.ResponsiveRow(
                    [
                        ft.Column(
                            [
                                self.niveaux,
                                ft.Text("Entrez vos thèmes  - séparez les par des virgules (,)", size=15, weight=ft.FontWeight.BOLD),
                                self.themes,
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
                                    on_click=lambda e: self.handle_close_qu,
                                    style=ft.ButtonStyle(bgcolor="#48dc03", color="#FFFFFF", overlay_color="#55ec04"),
                                ),
                                ft.FilledButton(
                                    text=" ",
                                    icon=ft.icons.QUESTION_MARK,
                                    width=65,
                                    height=45,
                                    on_click=lambda e: e.page.open(self.explication),
                                    style=ft.ButtonStyle(bgcolor="#009eff", color="#FFFFFF", overlay_color="#0190e8",),
                                ),
                            ],
                            spacing=10,  # Adjust spacing between buttons
                        ),
                    ],
                ),
            ],
        )


        if self.choice == "libre":
            self.value = rand_pick(self.libre)
        elif self.choice == "question":
            self.value = rand_pick(self.Questions)
        elif self.choice == "exercice":
            self.value = rand_pick(self.exercice)
        else:
            self.value = rand_pick(self.resume)

        self.fs = file_manager.FileSystem()
        if(self.fs.is_empty("assets/user_data/model_ai_user.txt")):
            self.first_time.visible = True

        self.prompt = ft.TextField(
            label=f"{self.value}", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=5,
            border_color="#FFFFFF",border_width=2, bgcolor="#272727", 
        )

        
        


        self.response_text = ft.Markdown()
        self.nom_fic = ft.TextField(label="Nom du fichier")

        self.drawer = ft.NavigationDrawer(
            on_change=self.handle_change,
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
                    icon=ft.Icon(ft.icons.MY_LIBRARY_BOOKS_OUTLINED),
                    label="Exercices",
                    selected_icon=ft.icons.MY_LIBRARY_BOOKS_ROUNDED,
                ),
                ft.NavigationDrawerDestination(
                    icon=ft.Icon(ft.icons.TEXT_SNIPPET_OUTLINED),
                    label="Fiches résumées",
                    selected_icon=ft.icons.TEXT_SNIPPET_ROUNDED,
                ),
            ],
        )

        self.dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmation"),
            content=ft.Text("Voulez vous sauvegardez votre prompt?"),
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



        

    def handle_close_qu(self, e):
        self.fs.append_file(self.niveaux.value, 0, "assets/user_data/user_log.txt")
        self.fs.append_file(self.themes.value.split(","), 1, "assets/user_data/user_log.txt")
        self.first_time.visible = False

    def handle_change(self, e):
        self.choice = e.control.selected_index
        print("change ")
        if self.choice == 0:
            self.choice = "libre"
            self.prompt.label = rand_pick(self.libre)
            print(self.prompt.label)


        elif self.choice == 1:
            self.prompt.label = "question"
            self.prompt.label = rand_pick(self.Questions)

        elif self.choice == 2:
            self.choice = "exercice"
            self.prompt.label = rand_pick(self.exercice)
        else:
            self.choice = "fiche"
            self.prompt.label = rand_pick(self.resume)

        self.update()


    def send_data(self, e, target_page):
        sleep(0.1)
        e.page.go(target_page)

    def AI_response(self, e, value):
        client = InferenceClient(api_key="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")
        preset = {
            "libre": "",
            "question": "Peux tu me faires des Questions sur le sujet suivant: ", 
            "exercice": "Peut tu me donner des exercices structurés différents et pertinents pour en acquérir les connaissance sur: ",
            "fiche": "Aide moi en faisant un résumé structuré sur: ",
        }

        print("prompt " + preset[value])
        print(value)

        messages = [
            {"role": "user", "content": f"{preset[value]} {self.prompt.value}"}
        ]

        stream = client.chat.completions.create(
            model="meta-llama/Meta-Llama-3-8B-Instruct",
            messages=messages, 
            temperature=0.5,
            max_tokens=6000,
            top_p=0.7,
            stream=True
        )

        if self.response_text.value is None:
            self.response_text.value = ""

        for chunk in stream:
            response_chunk = str(chunk.choices[0].delta.content)
            self.response_text.value += response_chunk  
            self.response_text.update()
            print(response_chunk, end="")
        self.prompt.value = ""

    def save(self, e):
        
        file_path = self.fs.write_to_file("./document/" + self.nom_fic.value + ".md", self.response_text.value)

        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Fichier sauvegardé: {self.nom_fic.value}")
        )
        e.page.snack_bar.open = True
        self.update()
        e.page.close(self.dlg_modal)
        sleep(1)

        value = randint(0, 10)
        old_xp = int(self.fs.read_given_line("assets/user_data/user_log.txt", 3))
        self.fs.append_file(str(int(value) + int(old_xp)), 3, file_path)
        e.page.snack_bar = ft.SnackBar(
            ft.Text(f"Vous avez gagné: {value} xp")
        )
        e.page.snack_bar.open = True
        self.update()

    def handle_close(self, e):
        e.page.close(self.dlg_modal)

    def build(self):
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
                                        on_click=lambda e: e.page.open(self.drawer),
                                        tooltip="Menu IA",
                                    ),
                                    ft.IconButton(
                                        icon=ft.icons.SAVE_ALT,
                                        icon_color="#FFFFFF",
                                        icon_size=30,
                                        on_click=lambda e: e.page.open(self.dlg_modal),
                                        tooltip="enregistrer",
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                    ),
                    self.first_time,
                    ft.Container(
                        ft.Column([self.response_text,], scroll=ft.ScrollMode.AUTO, ),
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
                                    self.prompt,
                                    ft.OutlinedButton(
                                        icon=ft.icons.ARROW_UPWARD,
                                        height=40,
                                        width=40,
                                        style=ft.ButtonStyle(
                                            color="#FFFFFF",
                                            overlay_color="#0190e8",
                                            shape=ft.RoundedRectangleBorder(radius=7),
                                        ),
                                        on_click=lambda e: self.AI_response(e, self.choice)  # Pass choice here
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


def feed(router_data: Union[Router, str, None] = None):
    return AIApp()
