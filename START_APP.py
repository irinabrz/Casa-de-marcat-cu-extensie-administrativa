import os
import sys
import django
import flet as ft
import asyncio
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
from UI_DASHBOARD import DashboardPage



def main(page : ft.Page):
    state = {
        "timpBlocare" : 30,
        "incercari" : 5
    }
    page.theme_mode = ft.ThemeMode.DARK
    page.title = "Introducere PIN angajat"
    page.window.width = 1024
    page.window.height = 768
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    pinDisplay = ft.Text("", size = 40, weight = "bold", color = "white")
    titlu = ft.Text("Introduceti codul pin:", size = 26, weight = "bold", color = "white")
    butoane = ft.Column(alignment="center")

    async def buttonClick(e):
        if e.control.data == "C":
            pinDisplay.value = ""
        elif e.control.data == "⌫":
            pinDisplay.value = pinDisplay.value[:-1]
        else:
            if len(pinDisplay.value) < 6:
                pinDisplay.value += e.control.data

        if len(pinDisplay.value) == 6:
            if pinDisplay.value == "111111":
                pinDisplay.color = "green"
                titlu.value = "Acces Permis!"
                print("Acces Permis!")
                page.update()
                await asyncio.sleep(0.5)
                page.clean()
                DashboardPage(page)
                

            else:
                pinDisplay.color = 'red'
                state["incercari"] -= 1
                if state["incercari"] == 0:
                    titlu.value = f"Prea multe incercari! Incearca din nou dupa {state['timpBlocare']} secunde!"
                    butoane.disabled = True
                    pinDisplay.value = ""
                    pinDisplay.color = 'white'
                    page.update()
                    await asyncio.sleep(state["timpBlocare"])
                    butoane.disabled = False
                    state["incercari"] = 5
                    state["timpBlocare"] *= 2
                    titlu.value = "Introduceti codul pin:"
                    page.update()
                else:
                    titlu.value = f"Pin Incorect! {state['incercari']} incercari ramase!"
                    butoane.disabled = True
                    page.update()
                    await asyncio.sleep(1)
                    butoane.disabled = False
                    pinDisplay.value = ""
                    pinDisplay.color = 'white'
        page.update()
    
    def creareButon(text):
        return ft.ElevatedButton(
            content = ft.Text(
                text,
                size = 30,
                weight = "bold",
                color = "white"
            ),
            data = text,
            width = 80,
            height = 80,
            style = ft.ButtonStyle(shape = ft.CircleBorder(), padding = 0),
            on_click = buttonClick
        )
    
    butoane.controls = [
        ft.Row([creareButon("1"), creareButon("2"), creareButon("3")], alignment="center"),
        ft.Row([creareButon("4"), creareButon("5"), creareButon("6")], alignment="center"),
        ft.Row([creareButon("7"), creareButon("8"), creareButon("9")], alignment="center"),
        ft.Row([creareButon("C"), creareButon("0"), creareButon("⌫")], alignment="center")
    ]

    page.add(
        ft.Container(content=titlu, alignment=ft.Alignment.CENTER),
        ft.Container(content=pinDisplay, alignment=ft.Alignment.CENTER, height=100),
        butoane
    )

if __name__ == "__main__":
    ft.app(target=main)