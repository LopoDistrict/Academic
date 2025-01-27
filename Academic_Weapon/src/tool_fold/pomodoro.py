import flet as ft

from . import file_manager

def pomodoro(router):
    fs = file_manager.FileSystem()

    class Pomodoro(ft.UserControl):
        def __init__(self):
            super().__init__()
            self.timer_duration = 25  # Default timer duration in minutes
            self.time_remaining = self.timer_duration * 60  # Time remaining in seconds
            self.running = False

            self.time_left = ft.Text(value=self.format_time(self.time_remaining), size=40, color="white")

            self.start_button = self.create_button("Débuter", self.start_timer)
            self.reset_button = self.create_button("Reset", self.reset_timer)

        def create_button(self, text, on_click):
            return ft.OutlinedButton(
                text=text,
                on_click=on_click,
                adaptive=True,
                width=150,
                height=50,
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    color="#FFFFFF",
                    overlay_color="#0b70d4",
                ),
                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
            )

        def build(self):
            return ft.Column(
                [
                    ft.Column([], spacing=55),
                    ft.Row(
                        [
                            self.create_timer_container("Travail", ["25 min.", "50 min."], [25, 50], "#ab0101"),
                            self.create_timer_container("Pause", ["5 min.", "15 min."], [5, 15], "#25a9b2"),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row([self.start_button, self.reset_button], alignment=ft.MainAxisAlignment.CENTER, height=115),
                    ft.Row([self.time_left], alignment=ft.MainAxisAlignment.CENTER),
                ]
            )

        def create_timer_container(self, title, button_texts, durations, bgcolor):
            return ft.Container(
                ft.Column(
                    [
                        ft.Text(title, size=30, weight=ft.FontWeight.BOLD),
                        *[self.create_duration_button(text, duration) for text, duration in zip(button_texts, durations)],
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=5,
                    width=170,
                ),
                bgcolor=bgcolor,
                width=150,
                border_radius=15,
                padding=15,
            )

        def create_duration_button(self, text, duration):
            return ft.FilledButton(
                text=text,
                on_click=lambda e: (self.set_timer(duration), self.bounce_animation(e)),
                adaptive=True,
                width=125,
                height=45,
                style=ft.ButtonStyle(
                    color="#FFFFFF",
                    bgcolor="#2a72b9",
                    overlay_color="#adb4ff",
                ),
                animate_scale=ft.Animation(duration=300, curve=ft.AnimationCurve.EASE_IN_OUT),
            )

        def bounce_animation(self, e):
            from time import sleep
            """Trigger a smooth bouncing animation on the clicked element."""
            e.control.scale = 1.2
            e.control.update()
            sleep(0.1)
            e.control.scale = 1.0
            e.control.update()

        def format_time(self, seconds):
            mins, secs = divmod(seconds, 60)
            return f"{mins:02}:{secs:02}"

        def set_timer(self, minutes):
            self.start_button.text = "Débuter"
            if self.running:
                self.running = False
            self.timer_duration = minutes
            self.time_remaining = self.timer_duration * 60
            self.time_left.value = self.format_time(self.time_remaining)
            self.update()

        def start_timer(self, e):
            if not self.running:
                self.running = True
                self.start_button.text = "Pause"
                self.update()
                self.run_timer()
            else:
                self.running = False
                self.start_button.text = "Continuer"
                self.update()
                self.write_time()

        def write_time(self):
            elapsed_time = self.timer_duration * 60 - self.time_remaining
            try:
                file_path = "assets/user_data/user_log.txt"
                old_xp = int(fs.read_given_line(file_path, 3))
                fs.append_file(str(elapsed_time + old_xp), 3, file_path)
                self.show_snackbar(f"Vous avez gagné: {elapsed_time} xp")
            except Exception as e:
                print(f"Error writing to file: {e}")

        def show_snackbar(self, message):
            try:
                self.page.snack_bar = ft.SnackBar(ft.Text(message))
                self.page.snack_bar.open = True
                self.page.update()
            except Exception as e:
                print(f"Error showing snackbar: {e}")

        def run_timer(self):
            from threading import Thread 
            def countdown():
                from time import sleep
                while self.time_remaining > 0 and self.running:
                    self.time_left.value = self.format_time(self.time_remaining)
                    self.update()
                    sleep(1)
                    self.time_remaining -= 1

                if self.running:
                    self.time_left.value = "00:00"
                    self.running = False
                    self.start_button.text = "Débuter"
                    self.update()
                    self.write_time()

            thread = Thread(target=countdown, daemon=True)
            thread.start()

        def reset_timer(self, e):
            self.running = False
            self.write_time()
            self.time_remaining = self.timer_duration * 60
            self.time_left.value = self.format_time(self.time_remaining)
            self.start_button.text = "Débuter"
            self.update()

    return Pomodoro()
