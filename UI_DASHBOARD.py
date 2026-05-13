import flet as ft
from UI_VANZARE import VanzarePage
from UI_STOCURI import StocuriPage


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
            StocuriPage(page)

    def creareButon(text, icon):
        return ft.ElevatedButton(
            content = ft.Container(
                content = ft.Column(
                    alignment = ft.MainAxisAlignment.CENTER,
                    horizontal_alignment= ft.MainAxisAlignment.CENTER,
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
