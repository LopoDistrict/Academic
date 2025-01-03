import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
from huggingface_hub import InferenceClient
from random import choice as rand_pick
from random import randint
from tool_fold import file_manager
from time import sleep
from openai import OpenAI
import time

class AIApp(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.choice = "libre"
        self.libre = ("Explique moi les matrices inversibles", "Parle moi du Droit international public", "Synthétise moi le conflit en Ukraine")
        self.Questions = ("cryptographie", "Droit des affaires", "Introduction au droit européen", "c++")
        self.resume = ("algorithme de dichotomie", "mécanique des fluides", "histologie-embryologie", "Biologie cellulaire")
        self.exercice = ("pivot de Gauss", "droit des personnes", "Matrice de permutation")
        self.value = ""
        self.interactive_reponse = ft.Markdown()
        self.response_text = ft.Markdown()
        #self.reponse_value = ft.Text(color="#0080ff")
        self.study_feed = ft.Column()
        self.current_study_index = 0
        self.start_y = None
        self.last_call_time = time.time()
        self.min_delay = 5  
        self.is_swiping = False
        #utile pour les qcm
        self.q1 = ft.OutlinedButton()
        self.q2 = ft.OutlinedButton()
        self.q3 = ft.OutlinedButton()
        self.q4 = ft.OutlinedButton()
        self.reponse_value = ft.Text(color="#0080ff")
        self.next_q = ft.FilledButton()

        self.smart = ft.Container(
                ft.GestureDetector(
                    content=ft.Column(
                        [
                            self.interactive_reponse,
                        ],
                        scroll=ft.ScrollMode.AUTO,  # Activer le défilement
                        expand=True,  # Permettre l'expansion du contenu
                    ),
                    on_pan_start=self.handle_pan_start,
                    on_pan_update=self.handle_pan_update, 
                    on_pan_end=self.handle_pan_end,  
                ),
                expand=True,
                visible=False,
                height=400,  # Définir une hauteur fixe pour le conteneur
                padding=10,
            )
        
        self.reponse = ft.Container(
                ft.Column([self.response_text,], scroll=ft.ScrollMode.AUTO, ),
                height=400,
                padding=10,
                #border=ft.border.all(2, ft.Colors.WHITE),
                border_radius=5,
                #bgcolor="#060606", 
                expand=True,
                visible=True
            )
        # Dropdown for levels
        self.niveaux = ft.Dropdown(
            width=225,
            hint_text="Entrez votre niveaux",
            options=[
                ft.dropdown.Option("Débutant"),
                ft.dropdown.Option("Intermédiaire"),
                ft.dropdown.Option("Difficile"),
                ft.dropdown.Option("Très difficile"),
                ft.dropdown.Option("Très Avancé"),
                ft.dropdown.Option("Le plus compliqué"),
            ],
        )

        # TextField for themes
        self.themes = ft.TextField(
            label="Themes ex(cryptographie,méca. fluide)", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=3,
            border_color="#FFFFFF", border_width=2
        )
        self.explication = ft.BottomSheet(
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
                        "Fermer", on_click=lambda e: e.page.close(self.explication)
                    ),
                ],
            ),
        ),
    )
        # AlertDialog for first-time setup
        self.first_time = ft.AlertDialog(
            modal=True,
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
                                    on_click=self.handle_close_qu,
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

        # Determine random choice
        if self.choice == "libre":
            self.value = rand_pick(self.libre)
        elif self.choice == "question":
            self.value = rand_pick(self.Questions)
        elif self.choice == "exercice":
            self.value = rand_pick(self.exercice)
        elif self.choice =="smart":
            self.prompt.label = "Entrez un sujet/matière"
        else:
            self.value = rand_pick(self.resume)

        self.fs = file_manager.FileSystem()


        self.prompt = ft.TextField(
            label=f"{self.value}", expand=True, border=ft.InputBorder.UNDERLINE, max_lines=5,
            border_color="#FFFFFF", border_width=2, bgcolor="#272727", 
        )


        
        self.nom_fic = ft.TextField(label="Nom du fichier")

        self.drawer = ft.NavigationDrawer(
            on_change=self.handle_change,
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
                ft.Text("Apprentissage personnalisé"),
                ft.NavigationDrawerDestination(
                    label="Système d'apprentissage intelligent",
                    icon=ft.Icons.SMART_TOY_OUTLINED,
                    selected_icon=ft.Icon(ft.Icons.SMART_TOY_ROUNDED),
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

    
        
    def handle_pan_start(self, e: ft.DragStartEvent):
        self.start_y = e.local_y  # Position verticale initiale
        self.is_swiping = True  # Indiquer qu'un swipe est en cours

    def handle_pan_update(self, e: ft.DragUpdateEvent):
        """
        Détecte un swipe vers le haut et appelle AI_response avec un délai minimum.
        """
        if self.start_y is None or not self.is_swiping:
            return

        delta_y = e.local_y - self.start_y

        if delta_y < -50:
            current_time = time.time()
            if current_time - self.last_call_time >= self.min_delay:
                #self.AI_response(e, self.choice)
                print("calling self.AI_response(e, self.choice)")
                print(f"self.last_call_time {self.last_call_time}")
                print(f"current_time {current_time}")
                self.last_call_time = current_time 
                self.is_swiping = False

    def handle_pan_end(self, e: ft.DragEndEvent):
        """
        Réinitialise l'indicateur de swipe lorsque le mouvement se termine.
        """
        self.is_swiping = False
        self.start_y = None


    def handle_close_qu(self, e):
        self.fs.append_file(self.niveaux.value, 6, "assets/user_data/user_log.txt")
        self.fs.append_file(self.themes.value.split(","), 7, "assets/user_data/user_log.txt")
        e.page.close(self.first_time)
        e.page.update()

    def handle_change(self, e):
        self.choice = e.control.selected_index
        print("change ")
        print(self.prompt.label)
        
        if self.choice == 1:
            self.choice = "libre"
            self.prompt.label = rand_pick(self.libre)
            print(self.prompt.label)

        elif self.choice == 2:
            self.prompt.label = "question"
            self.prompt.label = rand_pick(self.Questions)

        elif self.choice == 3:
            self.choice = "exercice"
            self.prompt.label = rand_pick(self.exercice)

        elif self.choice == 4:
            self.choice = "smart"
            self.smart.visible = True
            self.reponse.visible = False
            self.prompt.label = "Entrez un sujet/matière"
            e.page.update()
            #self.AI_response(e, self.choice)

        else:
            self.choice = "fiche"
            self.prompt.label = rand_pick(self.resume)

        e.page.update()

    def send_data(self, e, target_page):
        sleep(0.1)
        e.page.go(target_page)
        """

    def smartAI(self, e, value):
        client = OpenAI(base_url="https://api.zukijourney.com/v1", api_key='your-api-key-here')

        preset = {
            1: "Questions à choix multiples et la reponse précédé d'un -",
            2: "Une information intéressante qui pourait m'aider",
            3: "des questions en flash cards de la forme question,reponse "
        }
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": f"Afin de réussir un futur test sur {value} peut tu me donner"}]
        )"""


    def AI_response(self, e, value):
        print("AI_response")
        if self.smart.visible == True:
            print("l'ia reflechit")
            smart_client = OpenAI(base_url="https://api.zukijourney.com/v1", api_key='zu-95d68cdaf4f2ce1ea82fc9780f5a379b')
            smart_preset = {
                1: "Questions à choix multiples. Format: Q=Question, -=choix possible, R=Réponse",
                2: "Une information intéressante qui pourrait m'aider.",
                3: "juste des questions en flash cards. Format: Q=Question, R=Réponse"
            }
            choix = randint(1, 3)
            message = f"Afin de réussir un futur test sur {self.prompt.value} peut tu me donner {smart_preset[3]}"
            print(message)

            response = smart_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": message}]
            )

            print(response.choices[0].message.content)
            value =  (response.choices[0].message.content).replace("Q", "Question").replace("Réponse", "R")
            value = value.replace("**", "")
            if 3 == 3:
                #self.interactive_reponse.value = response.choices[0].message.content.replace("Q", "Question").replace("Réponse", "R")

                self.interactive_reponse.value = f"Je vous ai réalisé des flash Card sur {value}, retrouvée les dans l'onglet outils > flash cards"
                e.page.update()
                response_flash_card = value.split("Question")
                question_flash_card = value.split("Réponse")
                try:
                    for i in range(len(question_flash_card)):
                        temp_uniq_id = self.fs.uniq_id()    
                        self.fs.app_csv("assets/user_data/flash_card.csv", [temp_uniq_id, question_flash_card[i], response_flash_card[i]])
                except:
                    pass

            elif choix == 1:
                self.interactive_reponse.value = response.choices[0].message.content

            elif choix == 2:
                self.interactive_reponse.value = response.choices[0].message.content.replace("Q", "Question").replace("Réponse", "R")


            self.interactive_reponse.update()

        else:
            self.response_text.value = "l'IA réfléchit..."

            if not len(self.fs.read_given_line("assets/user_data/user_log.txt", 6).strip()):
                # If the choice hasn't been made, open the first-time setup dialog
                e.page.open(self.first_time)
                print("empty")
            else:
                client = InferenceClient(api_key="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")
                preset = {
                    "libre": "",
                    "question": "Peux tu me faires des Questions sur le sujet suivant: ", 
                    "exercice": "Peut tu me donner des exercices structurés différents et pertinents pour en acquérir les connaissance sur: ",
                    "fiche": "Aide moi en faisant un résumé structuré sur: ",
                }

                print("prompt " + preset[value])
                print(value)
                difficulte = "de cette difficulté: " + self.fs.read_given_line("assets/user_data/user_log.txt", 6)

                messages = [
                    {"role": "user", "content": f"{preset[value]} {self.prompt.value} {difficulte}"}
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

                self.response_text.value = ""
                self.response_text.update()

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
                    
                    self.reponse,
                    self.smart,
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
                                        on_click=lambda e: self.AI_response(e, self.choice) 
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