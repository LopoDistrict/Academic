import flet as ft
from . import file_manager
from time import sleep
from threading import Thread

def pomodoro(router):
    fs = file_manager.FileSystem()

    # Helper function to format time
    def format_time(seconds):
        mins, secs = divmod(seconds, 60)
        return f"{mins:02}:{secs:02}"

    # Timer state
    timer_duration = 25  # Default timer duration in minutes
    time_remaining = timer_duration * 60  # Time remaining in seconds
    running = False

    # UI components
    time_left = ft.Text(value=format_time(time_remaining), size=40, color="white")

    def create_button(text, on_click):
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

    def create_timer_container(title, button_texts, durations, bgcolor):
        return ft.Container(
            ft.Column(
                [
                    ft.Text(title, size=30, weight=ft.FontWeight.BOLD),
                    *[create_duration_button(text, duration) for text, duration in zip(button_texts, durations)],
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

    def create_duration_button(text, duration):
        return ft.FilledButton(
            text=text,
            on_click=lambda e: (set_timer(duration), bounce_animation(e)),
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

    def bounce_animation(e):
        """Trigger a smooth bouncing animation on the clicked element."""
        e.control.scale = 1.2
        e.control.update()
        sleep(0.1)
        e.control.scale = 1.0
        e.control.update()

    def set_timer(minutes):
        nonlocal timer_duration, time_remaining, running
        start_button.text = "Débuter"
        if running:
            running = False
        timer_duration = minutes
        time_remaining = timer_duration * 60
        time_left.value = format_time(time_remaining)
        time_left.update()

    def write_time():
        nonlocal time_remaining
        elapsed_time = timer_duration * 60 - time_remaining
        try:
            file_path = "assets/user_data/user_log.txt"
            old_xp = int(fs.read_given_line(file_path, 3))
            fs.append_file(str(elapsed_time + old_xp), 3, file_path)
            show_snackbar(f"Vous avez gagné: {elapsed_time} xp")
        except Exception as e:
            print(f"Error writing to file: {e}")

    def show_snackbar(message):
        try:
            page = time_left.page
            page.snack_bar = ft.SnackBar(ft.Text(message))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            print(f"Error showing snackbar: {e}")

    def run_timer():
        nonlocal time_remaining, running

        def countdown():
            nonlocal time_remaining, running
            while time_remaining > 0 and running:
                time_left.value = format_time(time_remaining)
                time_left.update()
                sleep(1)
                time_remaining -= 1

            if running:
                time_left.value = "00:00"
                running = False
                start_button.text = "Débuter"
                time_left.update()
                write_time()

        thread = Thread(target=countdown, daemon=True)
        thread.start()

    def start_timer(e):
        nonlocal running, time_remaining
        if not running:
            running = True
            start_button.text = "Pause"
            time_left.update()
            run_timer()
        else:
            running = False
            start_button.text = "Continuer"
            time_left.update()
            write_time()


    def reset_timer(e):
        nonlocal running, time_remaining
        running = False
        write_time()
        time_remaining = timer_duration * 60
        time_left.value = format_time(time_remaining)
        start_button.text = "Débuter"
        time_left.update()

    # Create buttons after all functions are defined
    start_button = create_button("Débuter", start_timer)
    reset_button = create_button("Reset", reset_timer)

    return ft.Column(
        [
            ft.Column([], spacing=55),
            ft.Row(
                [
                    create_timer_container("Travail", ["25 min.", "50 min."], [25, 50], "#ab0101"),
                    create_timer_container("Pause", ["5 min.", "15 min."], [5, 15], "#25a9b2"),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row([start_button, reset_button], alignment=ft.MainAxisAlignment.CENTER, height=115),
            ft.Row([time_left], alignment=ft.MainAxisAlignment.CENTER),
        ]
    )