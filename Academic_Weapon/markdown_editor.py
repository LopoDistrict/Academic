import flet as ft

def main(page: ft.Page):
    page.title = "Markdown Editeur"  # title of the AppBar with a white color
    page.theme_mode = "dark"    # dark mode
    page.adaptive = True

    page.navigation_bar = ft.NavigationBar(
        adaptive=True,
        bgcolor="#221d42",
        destinations=[
            ft.NavigationBarDestination(label="Outils", icon=ft.icons.EXPLORE, on_click=lambda _:page.go("pomodoro") ),
            ft.NavigationBarDestination(label="Communauté", icon=ft.icons.GROUP),
            ft.NavigationBarDestination(label="Librairie", icon=ft.icons.BOOKMARK),
        ],
    )

    def update_preview(e):
        """
        Updates the RHS(markdown/preview) when the content of the textfield changes.

        :param e: the event that triggered the function
        """
        md.value = text_field.value
        page.update()
    
    def handle_close(e):
        page.close(dlg_modal)

    def save(e):
        with open(f"document/{nom_fic.value}.txt", "w") as file:
            file.write(text_field.value)
            file.close()  
        page.close(dlg_modal)
        


    nom_fic = ft.TextField(label="Nom du fichier")
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Confirmation"),
        content=ft.Text("Voulez vous sauvegardez votre travail?"),
        actions=[
            ft.Column(
                [
                    nom_fic,
                ft.Row(
                    [
                        ft.TextButton("Oui", on_click=save),
                        ft.TextButton("Non", on_click=handle_close),
                    ],                    
                ),
                ],
                spacing=25,
            ),
            

        ],
    )
    def close_help(e):
        page.close(dlg_help)

    dlg_help = ft.AlertDialog(
        modal=True,
        title=ft.Text("Aide Markdown"),
        content=ft.Text("""
        _en italique_           # petit titre

        __en gras__             ## gros titre

        - une                   ### gros gros titre
        - liste
    
        - [x] liste             
        - [ ]  barré """),
        actions=[
            ft.Row(
                [
                    ft.TextButton("Fermer", on_click=close_help),
                ],                    
            ),
        ],
    )

    

    help_button = ft.FilledButton(
        text="aide",
        on_click=lambda _: page.open(dlg_help),
        adaptive=True,
        width=85,
        height=25,
        
        style=ft.ButtonStyle(bgcolor="#939cfc",),
    )

    save_button = ft.FilledButton(
        text="Enregistrer",
        on_click=lambda _: page.open(dlg_modal),
        adaptive=True,
        width=85,
        height=25,
        
        style=ft.ButtonStyle(bgcolor="#939cfc",),
    )

    text_field = ft.TextField(
        value="## Exemple MarkDown",  # the initial value in the field (a simple Markdown code to test)
        multiline=True,  # True means: it will be possible to have many lines of text
        on_change=update_preview,
        expand=True,  # tells the field to 'expand' (take all the available space)
        border_color=ft.colors.TRANSPARENT, # makes the border of the field transparent(invisible), creating an immersive effect
        label="Ecrivez vos notes ici",
    )
    
    md = ft.Markdown(
        value=text_field.value,  # make its value be equal to the content of our text_field
        selectable=True,  # to make the rendered markdown selectable
        extension_set="gitHubWeb",
        on_tap_link=lambda e: page.launch_url(e.data),
        
        # what happens when a link is clicked: a browser tab is opened up, with the link's URL
    )

    page.add(
        ft.Column(  # we use the row here, so everything fits on a line
            controls=[
                ft.Row(
                    [help_button,save_button],
                ),
                

                text_field,
                ft.Divider(height=5, color="white"),                
                ft.Container(  # we use the container here, to take advantage of its content alignment property
                    
                    ft.Column(  # we use the column here, to take advantage of its scroll property
                        [                            
                            md,
                                                                                    
                        ],
                        scroll="hidden",  # we make the Markdown scrollable
                    ),

                    expand=True,  # we make it fill up all the available space
                    alignment=ft.alignment.top_left,  # align the column
                )
                
            ],
            spacing=15,
            expand=True,  # we make it fill up all the available space
        )  # a row containing our text_field on the LHS and Markdown on the RHS
    )

    


ft.app(target=main)   # add parameter view=ft.WEB_BROWSER to show the output in your browser!