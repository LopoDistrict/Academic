import flet as ft
import datetime

def todo(router):
    class Task(ft.Column):
        def __init__(self, task_name, task_date, task_status_change, task_delete):
            super().__init__()
            self.completed = False
            self.task_name = task_name
            self.task_date = task_date
            self.task_status_change = task_status_change
            self.task_delete = task_delete
            self.display_task = ft.Checkbox(
                value=False, label=f"{self.task_name} • {self.task_date}", on_change=self.status_changed
            )
            self.edit_name = ft.TextField(expand=1)
            self.edit_date = ft.TextField(expand=1, value=self.task_date, label="Modifier la tâche (YYYY-MM-DD)")

            self.display_view = ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    self.display_task,
                    ft.Row(
                        spacing=0,
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.CREATE_OUTLINED,
                                tooltip="Edit To-Do",
                                on_click=self.edit_clicked,
                            ),
                            ft.IconButton(
                                ft.icons.DELETE_OUTLINE,
                                tooltip="Delete To-Do",
                                on_click=self.delete_clicked,
                            ),
                        ],
                    ),
                ],
            )

            self.edit_view = ft.Row(
                visible=False,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Column(
                        expand=1,
                        controls=[
                            self.edit_name,
                            self.edit_date,
                        ],
                    ),
                    ft.IconButton(
                        icon=ft.icons.DONE_OUTLINE_OUTLINED,
                        icon_color=ft.colors.GREEN,
                        tooltip="Update To-Do",
                        on_click=self.save_clicked,
                    ),
                ],
            )
            self.controls = [self.display_view, self.edit_view]

            

        def edit_clicked(self, e):
            self.edit_name.value = self.task_name
            self.edit_date.value = self.task_date
            self.display_view.visible = False
            self.edit_view.visible = True
            self.update()

        def save_clicked(self, e):
            self.task_name = self.edit_name.value
            self.task_date = self.edit_date.value
            self.display_task.label = f"{self.task_name} • {self.task_date}"
            self.display_view.visible = True
            self.edit_view.visible = False
            self.update()

        def status_changed(self, e):
            self.completed = self.display_task.value
            self.task_status_change(self)

        def delete_clicked(self, e):
            self.task_delete(self)

        


    class TodoApp(ft.Column):
        def __init__(self):
            super().__init__()

            self.new_task = ft.TextField(
                label="Nom de tâche", on_submit=self.add_clicked, expand=True,border=ft.InputBorder.UNDERLINE,max_length=25
            )

            self.selected_date = None
            self.date_picker_button = ft.ElevatedButton(
                "Choisir une Date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=self.show_date_picker,
                
            )

            self.tasks = ft.Column()

            self.filter = ft.Tabs(            
                scrollable=False,
                selected_index=0,
                on_change=self.tabs_changed,
                tabs=[ft.Tab(text="tâches")],            
            )

            self.items_left = ft.Text("0 tâches restantes")

            self.width = 600
            self.controls = [

                ft.Row(
                    controls=[
                        self.new_task,
                        ft.FloatingActionButton(
                            "Ajouter",
                            icon=ft.icons.ADD, on_click=self.add_clicked, bgcolor="#3B556D", 
                        ),
                    ],
                ),
                ft.Row(
                    controls=[
                        self.date_picker_button,
                    ],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[
                                self.items_left,
                            ],
                        ),
                    ],
                ),
            ]

        def show_date_picker(self, e):
            date_picker = ft.DatePicker(
                first_date=datetime.datetime(year=2023, month=10, day=1),
                on_change=self.date_changed,
                on_dismiss=self.handle_dismissal,
            )
            self.page.overlay.append(date_picker)  # Add the DatePicker to the overlay
            date_picker.open = True  # Open the DatePicker
            self.page.update()  # Update the page to reflect changes


        def date_changed(self, e):
            self.selected_date = e.control.value.strftime("%Y-%m-%d")
            self.page.snack_bar = ft.SnackBar(
                ft.Text(f"Date sélectionnée: {self.selected_date}")
            )
            self.page.snack_bar.open = True
            self.page.update()

        def handle_dismissal(self, e):
            self.page.snack_bar = ft.SnackBar(
                ft.Text("Sélection de la date rejetée.")
            )
            self.page.snack_bar.open = True
            self.page.update()

        def add_clicked(self, e):
            if self.new_task.value:
                task_date = self.selected_date or "pas de Date"
                task = Task(self.new_task.value, task_date, self.task_status_change, self.task_delete)
                self.tasks.controls.append(task)
                self.new_task.value = ""
                self.selected_date = None
                self.update()

        def task_status_change(self, task):
            self.update()

        def task_delete(self, task):
            self.tasks.controls.remove(task)
            self.update()

        def tabs_changed(self, e):
            self.update()

        def clear_clicked(self, e):
            for task in self.tasks.controls[:]:
                if task.completed:
                    self.task_delete(task)

        def before_update(self):
            status = self.filter.tabs[self.filter.selected_index].text
            count = 0
            for task in self.tasks.controls:
                task.visible = status == "tâches" or (status == "Completed" and task.completed)
                if not task.completed:
                    count += 1
            self.items_left.value = f"{count} tâches restantes"
    return TodoApp()



