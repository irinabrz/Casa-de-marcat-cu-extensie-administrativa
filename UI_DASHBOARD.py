import flet as ft
from UI_VANZARE import VanzarePage
from UI_STOCURI import StocuriPage
from UI_RAPOARTE import RapoartePage
from UI_MARFA import MarfaNouaPage


def DashboardPage(page : ft.Page):
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Dashboard Central"
    page.window.width = 1024
    page.window.height = 768
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def redirect(e):
        page.clean()
        if e.control.data == "Add Order":
            VanzarePage(page)
            
        elif e.control.data == "Management":
            page.add(
                ft.Column(
                    [
                        ft.Text("Meniu Management", size=26, weight="bold", color="white"),
                        ft.Container(height=20),
                        ft.Row(
                            [
                                creareButon("Stocuri", ft.Icons.INVENTORY),
                                creareButon("Marfă Nouă", ft.Icons.ADD_BOX),
                                creareButon("Rapoarte", ft.Icons.BAR_CHART),
                            ],
                            alignment="center",
                            spacing=40
                        ),
                        ft.Container(height=40),
                        ft.ElevatedButton(
                            "Înapoi la Meniu Principal", 
                            icon=ft.Icons.ARROW_BACK,
                            on_click=lambda _: [page.clean(), DashboardPage(page)]
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
            
        elif e.control.data == "Stocuri":
            StocuriPage(page)
        elif e.control.data == "Marfă Nouă":
            MarfaNouaPage(page)
        elif e.control.data == "Rapoarte":
            RapoartePage(page)

    def creareButon(text, icon):
        return ft.ElevatedButton(
            content = ft.Container(
                content = ft.Column(
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.CrossAxisAlignment.CENTER,
                    spacing = 20,
                    controls = [
                        ft.Icon(icon, color = 'white', size = 70),
                        ft.Text(value = text, color = 'white', size = 20)
                    ]
                ),
                expand = True
            ),
            data = text,
            on_click = redirect,
            style = ft.ButtonStyle(
                shape = ft.RoundedRectangleBorder(radius = 0),
                padding = 0
            ),
            width = 200,
            height = 200,
        )
    
    page.add(
        ft.Row(
            [
                creareButon("Add Order", ft.Icons.ADD),
                creareButon("Management", ft.Icons.STOREFRONT)
            ],
            alignment = "center",
            spacing = 80
        ) 
    )