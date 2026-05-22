import flet as ft
from FUNCTII_SQL import get_lista_produse_completa

def VanzarePage(page: ft.Page):
    butoaneProduse = ft.Row(wrap = True, spacing = 10, run_spacing = 10)
    listaProduse = ft.Column(scroll = ft.ScrollMode.ALWAYS, expand = True)
    produse = get_lista_produse_completa()

    def adaugareProdusCheckout(e):
        rand = ft.Row(
            controls = [
                ft.Text(e.control.data[0], size = 12, color = "white"),
                ft.Text(e.control.data[1], size = 12, color = "white"),
                ft.IconButton(
                    icon = ft.Icons.DELETE_ROUNDED,
                    icon_color = "red"
                ),
                ft.IconButton(icon = ft.Icons.REMOVE),
                ft.Text(value = '1', size = 12, color = "white"),
                ft.IconButton(icon = ft.Icons.ADD),
            ],
            alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        )
        
        listaProduse.controls.append(rand)
        page.update()

    def createButton(text, pret):
        pretConv = float(pret)
        return ft.ElevatedButton(
            content = ft.Text(
                text,
                size = 20,
                color = "white",
                weight = "bold",
                text_align = "center"
            ),
            width = 100,
            height = 100,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 0),
                padding = 0
            ),
            data = [text, pretConv],
            on_click = adaugareProdusCheckout
        )
    

    for produs in produse:
        butoaneProduse.controls.append(
            createButton(produs["nume_produs"], produs["pret"])
        )

    page.add(
        ft.Row(
            expand = True,
            controls = [
                ft.Container(
                    content = ft.Column([
                        ft.Text("Produse Disponibile"),
                        ft.Divider(),
                        butoaneProduse
                        ],
                    scroll = ft.ScrollMode.AUTO,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                expand = 2,
                padding = 20,
                border=ft.border.all(1, ft.Colors.OUTLINE),
                border_radius = 10
                ),

                ft.Container(
                    content = ft.Column([
                        ft.Text("Checkout"),
                        ft.Divider(),
                        listaProduse,
                        ft.Divider()
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    ),
                    expand = 1,
                    padding = 20,
                    bgcolor = ft.Colors.SURFACE_CONTAINER,
                    border_radius = 10
                )
            ]
        )


            #ft.Column([
            #    ft.Text("Sistem Casa de Marcat", size=25, weight="bold"),
            #    butoaneProduse
            #], expand=True)
    )
    