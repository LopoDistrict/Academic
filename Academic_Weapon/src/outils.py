import flet as ft
from typing import Union
from tool_fold.Router import Router, DataStrategyEnum
from State import global_state, State
from time import sleep
import os.path

def send_data(e, target_page):
    sleep(0.1)
    titles = {"/feed": 0, "/outil": 1, "/pomodoro": 1, "/": 2, "/about": 2, "/communaute": 3, "/librairie": 4}
    if target_page in titles:
        e.page.navigation_bar.selected_index = titles[target_page]
    e.page.go(target_page)
    e.page.update()

def bounce_animation(e):
    # Animate scaling up
    e.control.scale = 1.2
    e.control.update()

    # Wait for a short duration
    sleep(0.1)

    # Animate scaling back down
    e.control.scale = 1.0
    e.control.update()

def outils(router_data: Union[Router, str, None] = None):
    content = ft.Container(
        ft.Column(
            [
                ft.Text("Avec quoi nous travaillons aujourd'hui?", size=20, weight=ft.FontWeight.BOLD),
                ft.ResponsiveRow(
                    controls=[
                        ft.ElevatedButton(
                            icon=ft.icons.ACCESS_TIME,
                            text="Pomodoro",
                            width=60,
                            height=80,
                            on_click=lambda e: (bounce_animation(e), send_data(e, "/pomodoro")),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3974ab",
                                overlay_color="#0080ff",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.CHECKLIST,
                            text="Liste à faire",
                            width=60,
                            height=80,
                            on_click=lambda e: (bounce_animation(e), send_data(e, "/todo")),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3974ab",
                                overlay_color="#0080ff",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.EDIT,
                            text="Editeur de note Markdown",
                            width=60,
                            height=80,
                            on_click=lambda e: (bounce_animation(e), send_data(e, "/markdown_editor")),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3974ab",
                                overlay_color="#0080ff",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.FLIP,
                            text="Flash Cards",
                            width=60,
                            height=80,
                            on_click=lambda e: (bounce_animation(e), send_data(e, "/flash_cards")),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3974ab",
                                overlay_color="#0080ff",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.ACCOUNT_TREE_ROUNDED,
                            text="chat/aide IA",
                            width=60,
                            height=80,
                            on_click=lambda e: (bounce_animation(e), send_data(e, "/feed")),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#3974ab",
                                overlay_color="#0080ff",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.FilledButton(
                            icon=ft.icons.DRAW,
                            text="Notes en dessin[à venir]",
                            width=60,
                            height=80,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#253543",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.MULTITRACK_AUDIO_SHARP,
                            text="Note Audio[à venir]",
                            width=60,
                            height=80,
                            elevation=100,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#253543",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        ft.ElevatedButton(
                            icon=ft.icons.CALENDAR_MONTH,
                            text="Agenda [à venir]",
                            width=60,
                            height=80,
                            elevation=100,
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=10),
                                color="#FFFFFF",
                                bgcolor="#253543",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                    ],
                    run_spacing={"xs": 10},
                    columns=1,
                ),
            ],
            spacing=35,
            scroll=ft.ScrollMode.ALWAYS,
        ),
        height=1000,
    )
    return content
