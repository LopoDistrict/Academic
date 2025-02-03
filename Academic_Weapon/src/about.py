import flet as ft
from typing import Union
from time import sleep
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State


def send_data(e, target_page):
    sleep(0.1)
    titles = {"/feed": 0, "/outil": 1, "/pomodoro": 1, "/": 2, "/about": 2, "/communaute": 3, "/librairie": 4}

    e.page.navigation_bar.selected_index = titles[target_page]
    e.page.go(target_page)
    e.page.update()

def redirection(e, page):
    e.page.launch_url(page)

def about(router_data: Union[Router, str, None] = None):
    cond = """
    Conditions d'utilisation de l'application Academic Weapon
    En utilisant l'application Academic Weapon, vous acceptez les présentes conditions d'utilisation. Si vous n'acceptez pas ces conditions, veuillez ne pas utiliser l'application.

    1. Responsabilité des utilisateurs
    1.1 Publication de médias sur le "Hub"
    L'application Academic Weapon fournit un espace communautaire ("Hub") permettant aux utilisateurs de publier et de partager des médias. Cependant, Academic Weapon n'est pas responsable du contenu publié par les utilisateurs sur le Hub. Chaque utilisateur est entièrement responsable des médias qu'il publie.

    1.2 Respect et modération
    Tout média publié sur le Hub doit être respectueux et conforme aux lois en vigueur. Tout contenu incitant à la haine, à la violence, ou portant atteinte à la dignité d'autrui est strictement interdit. Academic Weapon se réserve le droit de supprimer tout contenu inapproprié et de bannir tout utilisateur ne respectant pas ces règles, sans préavis.

    2. Propriété intellectuelle
    2.1 Droits sur l'application
    L'application Academic Weapon, son design, son code source, ses fonctionnalités, et tout autre élément associé sont la propriété exclusive de Academic Weapon ou de ses concédants de licence. Vous n'êtes pas autorisé à copier, modifier, distribuer, ou exploiter ces éléments sans autorisation écrite préalable.

    2.2 Contenu des utilisateurs
    En publiant du contenu sur le Hub, vous conservez vos droits de propriété intellectuelle sur ce contenu. Cependant, vous accordez à Academic Weapon une licence mondiale, non exclusive, gratuite et transférable pour utiliser, reproduire, modifier, et afficher votre contenu dans le cadre de l'exploitation de l'application.

    3. Limitation de responsabilité
    3.1 Utilisation à vos risques
    L'application Academic Weapon est fournie "telle quelle". Nous ne garantissons pas que l'application sera exempte d'erreurs, de bugs, ou d'interruptions. Vous utilisez l'application à vos propres risques.

    3.2 Contenu tiers
    Academic Weapon n'est pas responsable des contenus publiés par des tiers sur le Hub, y compris les médias, les commentaires, ou les liens externes. Nous ne garantissons pas l'exactitude, la légalité, ou la qualité de ces contenus.

    4. Modifications des conditions d'utilisation
    Academic Weapon se réserve le droit de modifier ces conditions d'utilisation à tout moment. Les utilisateurs seront informés des changements majeurs, et la poursuite de l'utilisation de l'application après ces modifications constituera votre acceptation des nouvelles conditions.

    5. Loi applicable et juridiction
    Ces conditions d'utilisation sont régies par les lois en vigueur dans le pays où Academic Weapon est établie. Tout litige relatif à l'utilisation de l'application sera soumis à la juridiction compétente des tribunaux de ce pays.

    6. Contact
    Pour toute question ou réclamation concernant ces conditions d'utilisation, veuillez nous contacter à l'adresse suivante : kr0k0dilpepper@proton.me.

    En utilisant Academic Weapon, vous reconnaissez avoir lu, compris et accepté ces conditions d'utilisation.

    Dernière mise à jour : 19/01/2025
    """
    content = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            text="< Retour",
                            height=40,
                            width=110,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                                color="#FFFFFF",
                            ),
                            on_click=lambda e: send_data(e, "/")
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Text("Aidez moi!", size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(
                            """Cette application est totalement gratuite mais nous coute cher (IA, serveur, hébergement ...).
Pour nous aider vous pouvez me donnez de l'argent ou en partagez cette app auprès de vos potes.""",
                            size=13
                        ),
                        ft.Image(
                            src="assets/icons/qr_code.png",
                            width=90,
                            height=90,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                        )
                    ]
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.OutlinedButton(
                            text="un petit don? ❤️",
                            height=40,
                            width=110,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=5),
                                color="#FFFFFF",
                                bgcolor="#14e30e",
                            ),
                            on_click=lambda e: redirection(e, "Accueil")
                        ),
                        
                        ft.Row(
                            controls=[
                                ft.FilledButton(
                                    text="Twitter/X",
                                    height=40,
                                    width=110,                                    
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=5),                                
                                        color="#FFFFFF",
                                        bgcolor="#111111"
                                    ),
                                    on_click=lambda e: redirection(e, "https://x.com/Komodooo__")
                                ),
                                ft.FilledButton(
                                    text="Site Web ",
                                    height=40,
                                    width=110,
                                    style=ft.ButtonStyle(
                                        shape=ft.RoundedRectangleBorder(radius=5),
                                        color="#FFFFFF",
                                        bgcolor="#0080ff"
                                    ),
                                    on_click=lambda e: redirection(e, "https://academic-weapon.rf.gd")
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=15,
                        ),
                    ],
                ),
                ft.ResponsiveRow(
                    controls=[
                        ft.Markdown(
                            cond,
                            selectable=True,
                            extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
                        )
                    ],
                ),
                ft.Row(
                    controls=[
                        ft.Text("Ublonic_Order"),
                        ft.Image(
                            src="assets/icons/Ublonic_order.png",
                            width=70,
                            height=70,
                            repeat=ft.ImageRepeat.NO_REPEAT,
                        ),
                    ],
                ),
            ],
            spacing=35,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        expand=True,  # Ensure the container expands to fill the available space
    )

    return content
