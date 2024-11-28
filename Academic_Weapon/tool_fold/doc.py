import flet as ft
import pdf2image
from io import BytesIO
from PIL import Image as image
import numpy as np
import base64
import pypdf

def doc(router):
    i = 0
    fullname = ""  # Initialize the global variable for the file path

    def pick_files_result(e: ft.FilePickerResultEvent):
        nonlocal fullname  # Use nonlocal to modify the outer variable
        if e.files:
            fullname = e.files[0].path
            selected_files.value = f"Fichier sélectionné: {fullname}"
        else:
            fullname = ""
            selected_files.value = "Annulé!"
        selected_files.update()

    def btn_Click(e):
        nonlocal i, fullname

        if not fullname:
            cont.content = ft.Text("Pas de fichier sélectionné.")
            e.page.update()
            return

        try:
            src_pdf = pypdf.PdfReader(fullname)

            if i < 0:
                i = 0
            elif i >= len(src_pdf.pages):
                i = len(src_pdf.pages) - 1

            # Write the current page to a temporary file
            out = pypdf.PdfWriter()
            out.add_page(src_pdf.pages[i])
            temp_pdf = "t.pdf"
            with open(temp_pdf, "wb") as f:
                out.write(f)

            # Convert the temporary PDF to an image
            viewer = pdf2image.convert_from_path(temp_pdf, poppler_path=r"Library\bin")

            if not viewer:
                cont.content = ft.Text("Erreur dans le rendu du PDF.")
                e.page.update()
                return

            # Convert the first page to a base64 image
            arr = np.asarray(viewer[0])
            pil_img = image.fromarray(arr)
            buff = BytesIO()
            pil_img.save(buff, format="JPEG")
            pic = base64.b64encode(buff.getvalue()).decode("utf-8")

            cont.content = ft.Image(
                src_base64=pic,
                fit=ft.ImageFit.FILL,
            )
        except Exception as ex:
            cont.content = ft.Text(f"Erreur: {str(ex)}")
        finally:
            e.page.update()

    def btn_Next(e):
        nonlocal i
        i += 1
        btn_Click(e)

    def btn_Prev(e):
        nonlocal i
        i -= 1
        btn_Click(e)

    # File Picker
    pick_files_dialog = ft.FilePicker(on_result=pick_files_result)

    selected_files = ft.Text()

    # Viewer container
    cont = ft.Container(expand=1)

    # Buttons
    btn_load = ft.ElevatedButton(
        "Charger le fichier",
        icon=ft.icons.FILE_OPEN_ROUNDED,
        on_click=btn_Click,
    )

    btn_next = ft.ElevatedButton(
        "Prochaine page",
        icon=ft.icons.NAVIGATE_NEXT,
        on_click=btn_Next,
    )

    btn_prev = ft.ElevatedButton(
        "Page précédente",
        icon=ft.icons.NAVIGATE_BEFORE,
        on_click=btn_Prev,
    )

    # Page layout
    content = ft.Column(
        [
            ft.Row(
                [
                    ft.ElevatedButton(
                        "Choisir un fichier",
                        icon=ft.icons.UPLOAD_FILE,
                        on_click=pick_files_dialog.pick_files,
                    ),
                    selected_files,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            cont,
            ft.ResponsiveRow(
                [
                    btn_prev,
                    btn_load,
                    btn_next,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Add the FilePicker to the page
    router.page.add(pick_files_dialog)

    return content
