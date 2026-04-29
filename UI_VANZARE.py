import flet as ft

def VanzarePage(page: ft.Page):
    return ft.Column([
        ft.Text("Sistem Casa de Marcat", size=25, weight="bold"),
        ft.Text("Aici va fi interfața de vânzare-to do.")
    ], expand=True)