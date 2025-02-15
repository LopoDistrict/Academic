import flet as ft
from . import file_manager

def todo(router):
    class Task:
        def __init__(self, task_name, task_date, completed, task_status_change, task_delete):
            self.task_name = task_name
            self.task_date = task_date
            self.completed = completed
            self.task_status_change = task_status_change
            self.task_delete = task_delete
            self.fs = file_manager.FileSystem()

            self.display_task = ft.Checkbox(
                value=self.completed,
                label=f"{self.task_name} • {self.task_date}",
                on_change=self.status_changed
            )
            self.edit_name = ft.TextField(expand=1)
            self.edit_date = ft.TextField(
                expand=1, 
                value=self.task_date,
                label="Modifier la tâche (AAAA-MM-JJ)"
            )

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

            self.main_control = ft.Column(controls=[self.display_view, self.edit_view])

        def edit_clicked(self, e):
            self.edit_name.value = self.task_name
            self.edit_date.value = self.task_date
            self.display_view.visible = False
            self.edit_view.visible = True
            e.page.update()

        def save_clicked(self, e):
            old_row = [self.task_name, self.task_date, "1" if self.completed else "0"]
            new_row = [
                self.edit_name.value.replace('"', ""),
                self.edit_date.value.replace('"', ""),
                "1" if self.completed else "0"
            ]
            line = self.fs.search_line_csv("assets/user_data/to_do.csv", old_row)
            self.fs.replace_csv_row("assets/user_data/to_do.csv", line + 1, new_row)
            
            self.task_name = self.edit_name.value
            self.task_date = self.edit_date.value
            self.display_task.label = f"{self.task_name} • {self.task_date}"
            self.display_view.visible = True
            self.edit_view.visible = False
            e.page.update()

        def status_changed(self, e):
            self.completed = self.display_task.value
            self.task_status_change(self)
            old_row = [self.task_name, self.task_date, "1" if not self.completed else "0"]
            new_row = [self.task_name, self.task_date, "1" if self.completed else "0"]
            line = self.fs.search_line_csv("assets/user_data/to_do.csv", old_row)
            self.fs.replace_csv_row("assets/user_data/to_do.csv", line + 1, new_row)
            e.page.update()

        def delete_clicked(self, e):
            row_to_delete = [self.task_name, self.task_date, "1" if self.completed else "0"]
            line = self.fs.search_line_csv("assets/user_data/to_do.csv", row_to_delete)
            self.fs.delete_row_csv("assets/user_data/to_do.csv", line + 1)
            self.task_delete(self)

    class TodoApp:
        def __init__(self):
            self.fs = file_manager.FileSystem()
            self.new_task = ft.TextField(
                label="Nom de tâche",
                on_submit=self.add_clicked,
                expand=True,
                border=ft.InputBorder.UNDERLINE,
                max_length=25
            )
            self.selected_date = None
            self.task_objects = []
            
            self.date_picker_button = ft.ElevatedButton(
                "Choisir une Date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=self.show_date_picker,
            )
            
            self.tasks = ft.Column()
            self.items_left = ft.Text("0 tâches restantes")
            
            self.main_control = ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Column([], spacing=55),
                            self.new_task,
                            ft.FloatingActionButton(
                                "Ajouter",
                                icon=ft.icons.ADD,
                                on_click=self.add_clicked,
                                bgcolor="#3B556D",
                            ),
                        ]
                    ),
                    ft.Row(controls=[self.date_picker_button]),
                    ft.Column(
                        spacing=25,
                        controls=[
                            ft.Tabs(
                                scrollable=False,
                                selected_index=0,
                                on_change=self.tabs_changed,
                                tabs=[ft.Tab(text="tâches")]
                            ),
                            self.tasks,
                            ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[self.items_left]
                            )
                        ]
                    )
                ]
            )
            self.get_saved()

        def get_saved(self):
            try:
                tasks_saved = self.fs.matrix_csv("assets/user_data/to_do.csv")
                for row in tasks_saved:
                    if len(row) >= 3 and row[0] != "nom":
                        task = Task(
                            row[0],
                            row[1],
                            row[2].strip() == "1",
                            self.task_status_change,
                            self.task_delete
                        )
                        self.task_objects.append(task)
                        self.tasks.controls.append(task.main_control)
                self.update_items_left()
            except Exception as e:
                print(f"Error reading saved tasks: {e}")

        def show_date_picker(self, e):
            import datetime
            now = datetime.datetime.now()
            date_picker = ft.DatePicker(
                first_date=datetime.datetime(now.year, 1, 1),
                last_date=datetime.datetime(now.year + 1, 12, 31),
                on_change=self.date_changed,
                on_dismiss=self.handle_dismissal,
            )
            e.page.overlay.append(date_picker)
            date_picker.open = True
            e.page.update()

        def date_changed(self, e):
            self.selected_date = e.control.value.strftime("%Y-%m-%d")
            e.page.snack_bar = ft.SnackBar(ft.Text(f"Date sélectionnée: {self.selected_date}"))
            e.page.snack_bar.open = True
            e.page.update()

        def handle_dismissal(self, e):
            e.page.snack_bar = ft.SnackBar(ft.Text("Sélection de la date rejetée."))
            e.page.snack_bar.open = True
            e.page.update()

        def add_clicked(self, e):
            if self.new_task.value:
                task_date = self.selected_date or "pas de Date"
                value = [self.new_task.value, task_date, "0"]
                self.fs.app_csv("assets/user_data/to_do.csv", value)
                
                task = Task(
                    self.new_task.value,
                    task_date,
                    False,
                    self.task_status_change,
                    self.task_delete
                )
                self.task_objects.append(task)
                self.tasks.controls.append(task.main_control)
                self.new_task.value = ""
                self.selected_date = None
                self.update_items_left()
                e.page.update()

        def task_status_change(self, task):
            self.update_items_left()
            if self.items_left.page:
                self.items_left.page.update()

        def task_delete(self, task):
            if task in self.task_objects:
                self.task_objects.remove(task)
            if task.main_control in self.tasks.controls:
                self.tasks.controls.remove(task.main_control)
            self.update_items_left()
            if self.tasks.page:
                self.tasks.page.update()

        def tabs_changed(self, e):
            e.page.update()

        def update_items_left(self):
            remaining = sum(1 for task in self.task_objects if not task.completed)
            self.items_left.value = f"{remaining} tâches restantes"

    return TodoApp().main_control