import flet as ft
import datetime
from . import file_manager

def todo(router):
    class Task(ft.Column):
        def __init__(self, task_name, task_date, completed, task_status_change, task_delete):
            super().__init__()
            self.completed = completed
            self.task_name = task_name
            self.task_date = task_date
            self.task_status_change = task_status_change
            self.task_delete = task_delete
            self.fs = file_manager.FileSystem()
            self.display_task = ft.Checkbox(
                value=self.completed,  # Reflect saved completion state
                label=f"{self.task_name} • {self.task_date}",
                on_change=self.status_changed
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
            old_row = [self.task_name, self.task_date, "1" if self.completed else "0"]
            new_row = [(self.edit_name.value).replace('"', ""), (self.edit_date.value).replace('"', ""), "1" if self.completed else "0"]
            l = self.fs.search_line_csv("assets/user_data/to_do.csv", old_row)
            self.fs.replace_csv_row("assets/user_data/to_do.csv", l + 1, new_row)

            self.task_name = self.edit_name.value
            self.task_date = self.edit_date.value
            self.display_task.label = f"{self.task_name} • {self.task_date}"
            self.display_view.visible = True
            self.edit_view.visible = False
            self.update()

        def status_changed(self, e):
            self.completed = self.display_task.value
            self.task_status_change(self)
            old_row = [self.task_name, self.task_date, "1" if not self.completed else "0"]
            new_row = [self.task_name, self.task_date, "1" if self.completed else "0"]
            l = self.fs.search_line_csv("assets/user_data/to_do.csv", old_row)
            self.fs.replace_csv_row("assets/user_data/to_do.csv", l + 1, new_row)

        def delete_clicked(self, e):
            row_to_delete = [self.task_name, self.task_date, "1" if self.completed else "0"]
            l = self.fs.search_line_csv("assets/user_data/to_do.csv", row_to_delete)
            self.fs.delete_row_csv("assets/user_data/to_do.csv", l + 1)
            self.task_delete(self)

    class TodoApp(ft.Column):
        def __init__(self):
            super().__init__()
            self.fs = file_manager.FileSystem()
            self.new_task = ft.TextField(
                label="Nom de tâche", on_submit=self.add_clicked, expand=True, border=ft.InputBorder.UNDERLINE, max_length=25
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
                        ft.Column([], spacing=55),
                        self.new_task,
                        ft.FloatingActionButton(
                            "Ajouter",
                            icon=ft.icons.ADD, on_click=self.add_clicked, bgcolor="#3B556D",
                        ),
                    ],
                ),
                ft.Row(
                    controls=[self.date_picker_button],
                ),
                ft.Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            controls=[self.items_left],
                        ),
                    ],
                ),
            ]
            self.get_saved()

        def get_saved(self):
            try:
                tasks_saved = self.fs.matrix_csv("assets/user_data/to_do.csv")
                for row in tasks_saved:
                    if len(row) >= 3 and row[0] != "nom":
                        task_name = row[0]
                        task_date = row[1]
                        completed = row[2].strip() == "1"  # Ensure whitespace doesn't interfere
                        temp_task = Task(task_name, task_date, completed, self.task_status_change, self.task_delete)
                        self.tasks.controls.append(temp_task)
                self.update_items_left()
                self.update()
            except Exception as e:
                print(f"Error reading saved tasks: {e}")


        def show_date_picker(self, e):
            x = datetime.datetime.now()
            date_picker = ft.DatePicker(
                first_date=datetime.datetime(year=x.year, month=1, day=1),
                last_date=datetime.datetime(year=x.year + 1, month=12, day=31),
                on_change=self.date_changed,
                on_dismiss=self.handle_dismissal,
            )
            self.page.overlay.append(date_picker)
            date_picker.open = True
            self.page.update()

        def date_changed(self, e):
            self.selected_date = e.control.value.strftime("%Y-%m-%d")
            self.page.snack_bar = ft.SnackBar(ft.Text(f"Date sélectionnée: {self.selected_date}"))
            self.page.snack_bar.open = True
            self.page.update()

        def handle_dismissal(self, e):
            self.page.snack_bar = ft.SnackBar(ft.Text("Sélection de la date rejetée."))
            self.page.snack_bar.open = True
            self.page.update()

        def add_clicked(self, e):
            if self.new_task.value:
                task_date = self.selected_date or "pas de Date"
                value = [self.new_task.value, task_date, "0"]
                self.fs.app_csv("assets/user_data/to_do.csv", value)

                task = Task(self.new_task.value, task_date, False, self.task_status_change, self.task_delete)
                self.tasks.controls.append(task)
                self.new_task.value = ""
                self.selected_date = None
                self.update_items_left()
                self.update()

        def task_status_change(self, task):
            self.update_items_left()
            self.update()

        def task_delete(self, task):
            self.tasks.controls.remove(task)
            self.update_items_left()
            self.update()

        def tabs_changed(self, e):
            self.update()

        def update_items_left(self):
            remaining_tasks = sum(1 for task in self.tasks.controls if not task.completed)
            self.items_left.value = f"{remaining_tasks} tâches restantes"

    return TodoApp()
