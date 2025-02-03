import flet as ft
import datetime
from . import file_manager

def calendar(router):
    class Calendar(ft.Column):

        def __init__(self):
            super().__init__()
            self.x = datetime.datetime.now()
            self.map_days = {"Monday": 0, "Tuesday": 1, 
                            "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5,
                            "Sunday": 6}

            self.actual_day = self.x.strftime("%d")
            self.date_debut_semaine = self.x - datetime.timedelta(days=self.map_days[self.x.strftime("%A")])
            self.date_fin_semaine = self.x + datetime.timedelta(days=6-self.map_days[self.x.strftime("%A")])
            
            self.date_picker = ft.DatePicker(
                first_date=datetime.datetime(year=self.x.year, month=1, day=1),
                last_date=datetime.datetime(year=self.x.year + 1, month=12, day=31),
                on_change=self.date_picker_change
            )

            self.open_date_picker = ft.ElevatedButton(
                "Nouvelle evenement",
                on_click=lambda e: self.show_date(e)
            )

            self.titre = ft.TextField(
                label="Titre", border=ft.InputBorder.UNDERLINE, max_length=25
            )
            self.description = ft.TextField(
                label="Description", border=ft.InputBorder.UNDERLINE, max_length=100,
                multiline=True,
            )

            self.title_aff = ft.Text(size=23, weight=ft.FontWeight.BOLD)
            self.desc_aff = ft.Text(size=14, color="#ababab")
            self.date_aff = ft.Text(size=16, weight=ft.FontWeight.BOLD)
            
            self.nv_event = ft.AlertDialog(
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.CLOSE,
                                        icon_color="#FFFFFF",
                                        icon_size=20,
                                        on_click=lambda e: e.page.close(self.nv_event),
                                    )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                                ft.ResponsiveRow(
                                [
                                    self.titre,
                                    self.description,
                                    ft.FilledButton(
                                        text="Ajouter",
                                        icon=ft.icons.EDIT_CALENDAR_OUTLINED,
                                        on_click=lambda e: (self.display(self.date_picker.value, self.titre.value, self.description.value, False),
                                         e.page.close(self.nv_event), e.page.update()),
                                        width=125,
                                        height=45,
                                        style=ft.ButtonStyle(bgcolor="#48dc03", color="#FFFFFF", overlay_color="#55ec04"),
                                    ),                              
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        height=300,
                        spacing=20,
                    ),
                ),
            )

            self.info = ft.AlertDialog(
                content=ft.Container(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.icons.CLOSE,
                                        icon_color="#FFFFFF",
                                        icon_size=20,
                                        on_click=lambda e: e.page.close(self.info),
                                    )
                                ],
                                vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                                ft.ResponsiveRow(
                                [
                                    self.title_aff,                                
                                    self.desc_aff,
                                    self.date_aff,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        height=200,
                        spacing=20,
                    ),
                ),
            )
            
            self.lundi = ft.Column([ft.Text("Lundi", weight=ft.FontWeight.BOLD, size=17)])
            self.mardi = ft.Column([ft.Text("Mardi", weight=ft.FontWeight.BOLD, size=17)])
            self.mercredi = ft.Column([ft.Text("Mercredi", weight=ft.FontWeight.BOLD, size=17)])
            self.jeudi = ft.Column([ft.Text("Jeudi", weight=ft.FontWeight.BOLD, size=17)])
            self.vendredi = ft.Column([ft.Text("Vendredi", weight=ft.FontWeight.BOLD, size=17)])
            self.samedi = ft.Column([ft.Text("Samedi", weight=ft.FontWeight.BOLD, size=17)])
            self.dimanche = ft.Column([ft.Text("Dimanche", weight=ft.FontWeight.BOLD, size=17)])
            self.fs = file_manager.FileSystem()

            self.var_equi = {0 : self.lundi, 1: self.mardi, 
                            2: self.mercredi, 3: self.jeudi, 4: self.vendredi, 5: self.samedi, 6: self.dimanche}

            self.semaine = ft.Text(f'Semaine du {self.date_debut_semaine.strftime("%d/%m")} - {self.date_fin_semaine.strftime("%d/%m")}')
            self.controls = [
                ft.ResponsiveRow(
                    controls=[
                        self.info,
                        self.nv_event,
                        self.open_date_picker,
                        ft.Text("Calendrier", weight=ft.FontWeight.BOLD, size=22),
                        ft.Divider(height=20, color="transparent"),                           
                        self.lundi,
                        ft.Divider(height=10, thickness=3),
                        self.mardi,
                        ft.Divider(height=10, thickness=3),
                        self.mercredi,
                        ft.Divider(height=10, thickness=3),
                        self.jeudi,
                        ft.Divider(height=10, thickness=3),
                        self.vendredi,
                        ft.Divider(height=10, thickness=3),
                        self.samedi,
                        ft.Divider(height=10, thickness=3),
                        self.dimanche,                        
                        ft.Divider(height=20, color="transparent"), 
                        self.semaine,
                    ]
                ),
                ft.Row(
                    [
                        ft.FilledButton(     
                            text=" ",                       
                            icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                            icon_color="#FFFFFF",
                            width=140,
                            height=35,
                            on_click=lambda e: (self.bounce_animation(e), self.date_moins()),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=15),
                                color="#FFFFFF",
                                bgcolor="#3B556D",
                                overlay_color="#0b70d4",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                        
                        ft.FilledButton(     
                            text=" ",                       
                            icon=ft.Icons.ARROW_FORWARD_IOS,
                            icon_color="#FFFFFF",
                            width=140,
                            height=35,
                            on_click=lambda e: (self.bounce_animation(e), self.date_plus()),
                            style=ft.ButtonStyle(
                                shape=ft.RoundedRectangleBorder(radius=15),
                                color="#FFFFFF",
                                bgcolor="#3B556D",
                                overlay_color="#0b70d4",
                            ),
                            animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                ft.Divider(height=100, color="transparent"), 
            ]

        def empty_col(self):
            self.lundi.controls = [ft.Text("Lundi", weight=ft.FontWeight.BOLD, size=17)]
            self.mardi.controls = [ft.Text("Mardi", weight=ft.FontWeight.BOLD, size=17)]
            self.mercredi.controls = [ft.Text("Mercredi", weight=ft.FontWeight.BOLD, size=17)]
            self.jeudi.controls = [ft.Text("Jeudi", weight=ft.FontWeight.BOLD, size=17)]
            self.vendredi.controls = [ft.Text("Vendredi", weight=ft.FontWeight.BOLD, size=17)]
            self.samedi.controls = [ft.Text("Samedi", weight=ft.FontWeight.BOLD, size=17)]
            self.dimanche.controls = [ft.Text("Dimanche", weight=ft.FontWeight.BOLD, size=17)]

        def date_plus(self):
            self.empty_col()
            self.date_debut_semaine = self.date_debut_semaine + datetime.timedelta(days=7)
            self.date_fin_semaine = self.date_fin_semaine + datetime.timedelta(days=7)
            
            self.semaine.value = f'Semaine du {self.date_debut_semaine.strftime("%d/%m")} - {self.date_fin_semaine.strftime("%d/%m")}'
            self.load()

        def date_moins(self):
            self.empty_col()
            self.date_debut_semaine = self.date_debut_semaine - datetime.timedelta(days=7)
            self.date_fin_semaine = self.date_fin_semaine - datetime.timedelta(days=7)

            self.semaine.value = f'Semaine du {self.date_debut_semaine.strftime("%d/%m")} - {self.date_fin_semaine.strftime("%d/%m")}'
            self.load()

        def load(self):
            saved_dates = self.fs.read_matrix_json("assets/user_data/agenda.json")
            for i in range(len(saved_dates)):
                event_date = datetime.datetime.strptime(saved_dates[i][2], "%Y-%m-%d")
                if self.date_debut_semaine <= event_date <= self.date_fin_semaine:
                    self.display(event_date, saved_dates[i][0], saved_dates[i][1], True)
            self.page.update()

        def save(self, title, desc, date):
            value = {"id": f"{self.fs.uniq_id()}", "titre": title, "desc": desc, "date": str(date.strftime("%Y-%m-%d"))}
            self.fs.add_json_list("assets/user_data/agenda.json", value)

        def show_act(self, e, title, description, date):
            self.title_aff.value = title 
            self.desc_aff.value = description
            self.date_aff.value = date.strftime("%d/%m/%Y")
            e.page.open(self.info)
            e.page.update()

        def display(self, date, title, desc, is_write):
            date += datetime.timedelta(days=1)
            if not is_write:
                self.save(title, desc, date)
            if self.date_debut_semaine <= date <= self.date_fin_semaine:
                delta = (date - self.date_debut_semaine).days
                tache = ft.Container(
                    content=ft.Column([
                        ft.Text(title, weight=ft.FontWeight.BOLD),
                        ft.Text(desc[0:15] + "...")
                    ]),
                    bgcolor=self.fs.get_random_hex_color(),
                    on_click=lambda e: self.show_act(e, title, desc, date),
                    border_radius=15,
                    padding=10
                )
                self.var_equi[delta].controls.append(tache)

                self.page.update()

        def show_date(self, e):
            self.page.overlay.append(self.date_picker)
            self.date_picker.open = True
            self.page.update()

        def date_picker_change(self, e):
            self.page.dialog = self.nv_event
            self.nv_event.open = True
            self.page.update()

        def bounce_animation(self, e):
            from time import sleep
            e.control.scale = 1.2
            e.control.update()

            # Wait for a short duration
            sleep(0.1)

            # Animate scaling back down
            e.control.scale = 1.0
            e.control.update()

    calendar_component = Calendar()
    router.page.overlay.append(calendar_component.date_picker)  # Add DatePicker to overlay
    calendar_component.page = router.page  # Set the page reference
    calendar_component.load()  # Load events
    router.page.update()  # Update the page

    return calendar_component