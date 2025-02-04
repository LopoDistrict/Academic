import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
import datetime
from tool_fold import file_manager
from random import randint, choice

def send_data(e, target_page):
    from time import sleep
    sleep(0.1)
    titles = {"/feed": 0, "/outil": 1, "/pomodoro": 1, "/": 2, "/about": 2, "/communaute": 3, "/librairie": 4}

    e.page.navigation_bar.selected_index = titles[target_page]
    e.page.go(target_page)
    e.page.update()

def is_nv_streak():
    from random import randint
    fs = file_manager.FileSystem()

    last_connection_str = fs.read_given_line("assets/user_data/user_log.txt", 2).strip()
    last_connection = datetime.datetime.strptime(last_connection_str, "%Y/%m/%d")

    actual_date = datetime.datetime.now().date()

    fs.append_file(actual_date.strftime("%Y/%m/%d"), 2, "assets/user_data/user_log.txt")
    anc = int(fs.read_given_line("assets/user_data/user_log.txt", 0).strip())

    days_diff = (actual_date - last_connection.date()).days

    if days_diff >= 2:
        fs.append_file("0", 0, "assets/user_data/user_log.txt")
        return "0"

    if days_diff >= 1:
        new_streak = anc + 1
        fs.append_file(str(new_streak), 0, "assets/user_data/user_log.txt")
        old_xp = fs.read_given_line('assets/user_data/user_log.txt', 3)

        fs.append_file(str(int(old_xp) + randint(9, 15)), 3, 'assets/user_data/user_log.txt')  # on lui ajoute de l'xp

        return new_streak
    else:
        return anc

def bounce_animation(e):
    from time import sleep
    # Animate scaling up
    e.control.scale = 1.2
    e.control.update()

    # Wait for a short duration
    sleep(0.1)

    # Animate scaling back down
    e.control.scale = 1.0
    e.control.update()

def accueil(router_data: Union[Router, str, None] = None):
    def get_level(e=None):
        fs = file_manager.FileSystem()
        exp = int(fs.read_given_line("assets/user_data/user_log.txt", 3))
        exp_value = (0, 15, 35, 55, 75, 100, 250, 310, 480, 560, 700, 820, 1000, 1780, 2100, 2690, 3100, 4850, 6013)
        grade = ("barabare capable", "guerrier savant", "magicien intelligent", "mousquetaire averti", "Hallebardier éduqué",
            "saltinbamque doué", "évêque précheur", "Chewa savant", "paladin perspicace", "amazone clairvoyante", "janissaires doué", "tsar instruit",
            "sultan éclairé", "Danseur de l'ombre senior", "Invocateur réfléchi", "fou ordonné", "malin génie","démon malin"
            "puissance divine raisonnable", "È›g?œÆ'sd¸a19‹ˆoP$¾Þ!  ¸ä½€‚†£Jã«ò«F")
        for i in range(len(exp_value)):
            if exp >= exp_value[i]:
                if i + 1 < len(exp_value) and exp >= exp_value[i + 1]:
                    continue
                else:
                    fs.append_file(str(i + 1) + "-" + grade[i], 4, "assets/user_data/user_log.txt")
                    if e:
                        e.page.open(streak_bottom)
                    return i + 1

    fs = file_manager.FileSystem()
    streak_bottom = ft.BottomSheet(
        dismissible=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(
                        "L'experience (ou xp) s'acquiet avec le temps et le travail, plus vous vous connectez et travaillez plus vous en gagnez. A la longue vous obteindrez un grade.",
                        size=15,
                    ),
                    ft.ElevatedButton(
                        "Fermer",
                        on_click=lambda e: (bounce_animation(e), e.page.close(streak_bottom)),
                        animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                    ),
                ],
            ),
        ),
    )

    work_streak = ft.BottomSheet(
        dismissible=True,
        content=ft.Container(
            padding=50,
            content=ft.Column(
                tight=True,
                controls=[
                    ft.Text(
                        "Le work streak vous pousse à la régularité et à la discipline dans votre Travail. Chaque fois que vous vous connectez de suite vous obtenez de l'expérience et vous éliminez votre procratination. ",
                        size=15,
                    ),
                    ft.ElevatedButton(
                        "Fermer",
                        on_click=lambda e: (bounce_animation(e), e.page.close(work_streak)),
                        animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                    ),
                ],
            ),
        ),
    )

    from random import choice
    get_level()

    x = datetime.datetime.now()
    hour = int(x.strftime("%H"))
    if 6 <= hour <= 12:
        value_hour = "Bonjour "
    elif 12 <= hour <= 18:
        value_hour = "Bon Après midi "
    else:
        value_hour = "Bonsoir "

    val_temp = is_nv_streak()

    # Main content
    matieres = ("maths", "bio", "info", "medecine", "anglais", "géo", "éco", "droit", "chimie", "philo")
    content = ft.Container(
        content=ft.Column(
            [
                ft.ResponsiveRow(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.IconButton(
                                    icon=ft.icons.INFO_OUTLINED,
                                    icon_color="#FFFFFF",
                                    icon_size=20,
                                    on_click=lambda e: (bounce_animation(e), send_data(e, "/about")),
                                    animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                                ),
                                ft.Text(value_hour + fs.read_given_line("assets/user_data/user_log.txt", 5), size=30, weight=ft.FontWeight.BOLD),
                            ],
                        ),
                    ],
                    spacing=0,
                ),

                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text("Work Streak", size=25, weight=ft.FontWeight.BOLD),
                            ft.Icon(
                                name=ft.icons.LOCAL_FIRE_DEPARTMENT,
                                color="#e50000",
                                size=35,
                            ),
                            ft.Text(f"{val_temp}", size=19, weight=ft.FontWeight.BOLD),
                        ],
                        spacing=20,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    on_click=lambda e: (bounce_animation(e), e.page.open(work_streak)),
                    height=60,
                    bgcolor="#0080ff",
                    padding=ft.padding.only(left=10),
                    animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                ),
                ft.Divider(height=20, color="transparent"),
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Entrainement mentale 🧠", size=17, weight=ft.FontWeight.BOLD),
                            ft.Text("Renforcez vos connaissances et capacités avec le Feed, s'échauffer sur: "),
                            ft.OutlinedButton(
                                icon=ft.icons.AUTO_STORIES,
                                text=choice(matieres),
                                icon_color="#FFFFFF",
                                on_click=lambda e: (bounce_animation(e), send_data(e, "/feed")),
                                height=50,
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    overlay_color="#1d5384",
                                    color="#FFFFFF",
                                ),
                                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            ),
                        ]
                    ),
                ),
                # Spacing between containers
                ft.Divider(height=20, color="transparent"),  # Add spacing
                # Work Time Container
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text(
                                "Heure travaillé ⏲️: "
                                + str(int(fs.read_given_line("assets/user_data/user_log.txt", 1)) / 60)[
                                    0:4
                                ]
                                + " min.",
                                size=17,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text("Ne perdez pas votre concentration continuez à travailler"),
                            ft.OutlinedButton(
                                icon=ft.icons.ACCESS_TIME,
                                text="Continuer à travailler",
                                on_click=lambda e: (bounce_animation(e), send_data(e, "/pomodoro")),
                                height=50,
                                icon_color="#FFFFFF",
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    overlay_color="#1d5384",
                                    color="#FFFFFF"
                                ),
                                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            ),
                        ],
                        spacing=20,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    height=110,
                ),
                # Spacing between containers
                ft.Divider(height=20, color="transparent"),  # Add spacing
                # Last Document Container
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Dernier Document Travaillé📚 ", size=17, weight=ft.FontWeight.BOLD),
                            ft.FilledButton(
                                text=f"{fs.get_last_modified()}",
                                icon=ft.icons.INSERT_DRIVE_FILE,
                                width=60,
                                height=40,
                                icon_color="#FFFFFF",
                                on_click=lambda e: (bounce_animation(e), send_data(e, "/librairie")),
                                style=ft.ButtonStyle(
                                    shape=ft.RoundedRectangleBorder(radius=10),
                                    color="#FFFFFF",
                                    bgcolor="#3B556D",
                                    overlay_color="#0b70d4",
                                ),
                                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    height=50,
                ),
                # Spacing between containers
                ft.Divider(height=20, color="transparent"),  # Add spacing
                # XP and Levels Container
                ft.Container(
                    content=ft.ResponsiveRow(
                        [
                            ft.Text("Xp et levels ⚔️", size=20, weight=ft.FontWeight.BOLD),
                            ft.Text(
                                f"Experience acquis : {str(fs.read_given_line('assets/user_data/user_log.txt', 3))}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Niveau : {str(fs.read_given_line('assets/user_data/user_log.txt', 4).split("-")[0])}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"Classe : {str(fs.read_given_line('assets/user_data/user_log.txt', 4).split("-")[1])}",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.FilledButton(
                                text="Information à propos de l'xp",
                                on_click=lambda e: (bounce_animation(e), e.page.open(streak_bottom)),
                                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                            ),
                        ],
                    ),
                    border_radius=15,
                    border=ft.border.all(2, ft.Colors.WHITE),
                    bgcolor="#55a7f3",
                    padding=10,
                ),
            ],
            spacing=25,  # No spacing between main elements
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=400,
        height=1100,
        padding=ft.padding.all(10),
        border_radius=20,
    )

    return content
