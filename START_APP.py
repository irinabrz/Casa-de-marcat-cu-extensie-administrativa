import os
import sys
import django
import flet as ft
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONFIG_SISTEM.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
try:
    django.setup()
except Exception as e:
    print(f"Eroare setup Django: {e}")
from UI_VANZARE import VanzarePage
from UI_STOCURI import StocuriPage
from UI_RAPOARTE import RapoartePage
from UI_MARFA import MarfaNouaPage

def main(page: ft.Page):
    page.title = "MDS Cafenea System"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 800
    
    main_view = ft.Container(
        content=ft.Column([
            ft.Text("Dashboard Central", size=40, weight="bold"),
            ft.Text("Te rog selectează o opțiune de mai sus", size=20, color="black"),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        expand=True,
        padding=50
    )
    def mergi_la_vanzare(e):
        main_view.content = VanzarePage(page)
        page.update()

    def mergi_la_stocuri(e):
        main_view.content = StocuriPage(page)
        page.update()

    def mergi_la_rapoarte(e):
        main_view.content = RapoartePage(page)
        page.update()
    def mergi_la_marfa(e):
        main_view.content = MarfaNouaPage(page)
        page.update()
    header = ft.Container(
    content=ft.Row([
        ft.ElevatedButton("Vânzari", on_click=mergi_la_vanzare, bgcolor="blue", color="white"),
        ft.ElevatedButton("Stocuri", on_click=mergi_la_stocuri, bgcolor="orange", color="white"),
        ft.ElevatedButton("Marfă Nouă", on_click=mergi_la_marfa, bgcolor="pink", color="white"),
        ft.ElevatedButton("Rapoarte", on_click=mergi_la_rapoarte, bgcolor="purple", color="white"),
    ], alignment=ft.MainAxisAlignment.CENTER),
    padding=20,
    bgcolor="white"
)
    footer = ft.Row(
        [ft.Text("Zi frumoasa!", size=16, italic=True)],
        alignment=ft.MainAxisAlignment.CENTER
    )

    page.add(
        header,
        ft.Divider(height=20),
        main_view,
        ft.Divider(),
        footer
    )

if __name__ == "__main__":
    ft.app(target=main)