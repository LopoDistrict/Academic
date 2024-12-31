import flet as ft
import flet.canvas as cv
from PIL import Image, ImageDraw
import os

# Ensure the document directory exists
os.makedirs("./document", exist_ok=True)

class State:
    x: float
    y: float
    current_color: str = ft.colors.BLACK
    pen_size: int = 3
    is_highlighting: bool = False

state = State()

def main(page: ft.Page):
    page.title = "Note-Taking and Drawing App"
    page.padding = 10
    page.theme_mode = ft.ThemeMode.LIGHT  # Set theme to light mode

    def pan_start(e: ft.DragStartEvent):
        state.x = e.local_x
        state.y = e.local_y

    def pan_update(e: ft.DragUpdateEvent):
        color = state.current_color
        if state.is_highlighting:
            color = ft.colors.YELLOW + "80"  # Semi-transparent yellow for highlighting
        cp.shapes.append(
            cv.Line(
                state.x, state.y, e.local_x, e.local_y, paint=ft.Paint(stroke_width=state.pen_size, color=color)
            )
        )
        cp.update()
        state.x = e.local_x
        state.y = e.local_y

    def change_pen_size(size: int):
        state.pen_size = size
        page.update()

    def change_color(color: str):
        state.current_color = color
        state.is_highlighting = False
        page.update()

    def toggle_highlight():
        state.is_highlighting = not state.is_highlighting
        page.update()

    def save_canvas():
        if not cp.shapes:
            page.snack_bar = ft.SnackBar(ft.Text("No content to save!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            # Get the canvas dimensions
            canvas_width = int(cp.width) if cp.width else 600  # Default to 600 if width is None
            canvas_height = int(cp.height) if cp.height else 600  # Default to 600 if height is None
            # Create a blank image
            img = Image.new("RGB", (canvas_width, canvas_height), "white")
            draw = ImageDraw.Draw(img)
            # Draw each shape on the image
            for shape in cp.shapes:
                if isinstance(shape, cv.Line):
                    draw.line([(shape.x1, shape.y1), (shape.x2, shape.y2)], fill=shape.paint.color, width=shape.paint.stroke_width)
            # Save the image
            save_path = os.path.join("./document", "drawing.png")
            img.save(save_path)
            page.snack_bar = ft.SnackBar(ft.Text(f"Drawing saved to {save_path}"))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error saving drawing: {e}"))
            page.snack_bar.open = True
            page.update()

    def load_canvas():
        load_path = os.path.join("./document", "drawing.png")
        if not os.path.exists(load_path):
            page.snack_bar = ft.SnackBar(ft.Text("No saved drawing found!"))
            page.snack_bar.open = True
            page.update()
            return
        try:
            # Clear the canvas
            cp.shapes.clear()
            # Load the image and draw it on the canvas
            img = Image.open(load_path)
            img = img.convert("RGB")
            for x in range(img.width):
                for y in range(img.height):
                    r, g, b = img.getpixel((x, y))
                    if (r, g, b) != (255, 255, 255):  # Skip white pixels
                        cp.shapes.append(
                            cv.Line(x, y, x + 1, y + 1, paint=ft.Paint(stroke_width=1, color=ft.rgb(r, g, b)))
                        )
            cp.update()
            page.snack_bar = ft.SnackBar(ft.Text(f"Drawing loaded from {load_path}"))
            page.snack_bar.open = True
            page.update()
        except Exception as e:
            page.snack_bar = ft.SnackBar(ft.Text(f"Error loading drawing: {e}"))
            page.snack_bar.open = True
            page.update()

    # Canvas
    cp = cv.Canvas(
        [
            cv.Fill(
                ft.Paint(
                    gradient=ft.PaintLinearGradient(
                        (0, 0), (600, 600), colors=[ft.colors.CYAN_50, ft.colors.GREY]
                    )
                )
            ),
        ],
        content=ft.GestureDetector(
            on_pan_start=pan_start,
            on_pan_update=pan_update,
            drag_interval=10,
        ),
        expand=True,
    )

    # Toolbar
    toolbar = ft.ResponsiveRow(
        [
            ft.Dropdown(
                label="Pen Size",
                options=[
                    ft.dropdown.Option("1"),
                    ft.dropdown.Option("3"),
                    ft.dropdown.Option("5"),
                    ft.dropdown.Option("10"),
                ],
                value="3",
                on_change=lambda e: change_pen_size(int(e.control.value)),
                col={"sm": 6, "md": 3},
            ),
            ft.ElevatedButton("Black", on_click=lambda e: change_color(ft.colors.BLACK), col={"sm": 6, "md": 2}),
            ft.ElevatedButton("Red", on_click=lambda e: change_color(ft.colors.RED), col={"sm": 6, "md": 2}),
            ft.ElevatedButton("Blue", on_click=lambda e: change_color(ft.colors.BLUE), col={"sm": 6, "md": 2}),
            ft.ElevatedButton("Green", on_click=lambda e: change_color(ft.colors.GREEN), col={"sm": 6, "md": 2}),
            ft.ElevatedButton("Highlight", on_click=lambda e: toggle_highlight(), col={"sm": 6, "md": 3}),
            ft.ElevatedButton("Save", on_click=lambda e: save_canvas(), col={"sm": 6, "md": 3}),
            ft.ElevatedButton("Load", on_click=lambda e: load_canvas(), col={"sm": 6, "md": 3}),
        ],
        spacing=10,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Main layout
    page.add(
        ft.Column(
            [
                toolbar,
                ft.Container(
                    cp,
                    border_radius=5,
                    width=float("inf"),
                    height=600,
                    expand=True,
                ),
            ],
            spacing=10,
            expand=True,
        )
    )

ft.app(main)