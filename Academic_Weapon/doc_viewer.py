import flet as ft
import pdf2image
from io import BytesIO
from PIL import Image as image
import numpy as np
import base64

import pypdf

i = 0


def main(page: ft.Page):
    fullname = r'./placemeznt.pdf'
    src_pdf = pypdf.PdfReader(fullname)


    def btn_Click(e):
        global i

        if i >= len(src_pdf.pages):
            i = 0


        out = pypdf.PdfWriter()
        out.add_page(src_pdf.pages[i])
        out.write('t.pdf')

        viewer = pdf2image.convert_from_path('t.pdf',
                                             poppler_path=r'D:\Python\PDF-ORGANIZER\PDF2TIFF\poppler-24.02.0\Library\bin')
        viewer64 = []
        for view in viewer:
            arr = np.asarray(view)
            pil_img = image.fromarray(arr)
            buff = BytesIO()
            pil_img.save(buff, format="JPEG")
            pic = base64.b64encode(buff.getvalue()).decode("utf-8")
            viewer64.append(pic)

        cont.content = ft.Image(src_base64=viewer64[0],
            fit=ft.ImageFit.FILL,
            )
        page.update()


    cont = ft.Container(expand=1,
        border=ft.border.all(3, ft.colors.RED),)

    btn = ft.IconButton(
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda e: btn_Click(e),
        icon_size=35,)

    def btn_Next(e):
        global i
        i += 1
        btn_Click(e)

    btn_n = ft.IconButton(
        icon=ft.icons.NAVIGATE_NEXT,
        on_click=lambda e: btn_Next(e),
        icon_size=35,)


    page.add(ft.Column([cont, btn, btn_n],
        horizontal_alignment=ft.MainAxisAlignment.CENTER))
    page.window_maximized = True
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO
    page.update()

ft.app(target=main, assets_dir="assets")