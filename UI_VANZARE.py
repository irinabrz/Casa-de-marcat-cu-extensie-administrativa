import flet as ft
from LOGICA_DATABASE.models import Produs, Angajat
from FUNCTII_SQL import inregistreaza_vanzare

def VanzarePage(page: ft.Page):
    produse = Produs.objects.all()
    angajat = Angajat.objects.first()

    def finalizeaza(e):
        if not dropdown.value: return
        inregistreaza_vanzare(angajat.id, [{'id': int(dropdown.value), 'cantitate': 1}], "Cash")
        page.snack_bar = ft.SnackBar(ft.Text("Vânzare reușită în Oracle!"))
        page.snack_bar.open = True
        page.update()

    dropdown = ft.Dropdown(
        label="Alege Produs",
        options=[ft.dropdown.Option(key=str(p.id), text=p.nume_produs) for p in produse]
    )

    return ft.Column([
        ft.Text("Terminal Vânzare", size=25, weight="bold"),
        dropdown,
ft.ElevatedButton("Finalizează Tranzacție", on_click=finalizeaza, icon="check")    ])