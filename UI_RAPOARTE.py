""" MODUL: RAPOARTE ȘI STATISTICI
Scop: Vizualizare profit, grafice financiare și export PDF.
Cerința: 2.b, c, g, h) Statistici vizuale și rapoarte."""
import flet as ft
from FUNCTII_SQL import calculeaza_vanzari_astazi, get_raport_venituri, verifica_stocuri_critice

def RapoartePage(page: ft.Page):
    venit_azi = calculeaza_vanzari_astazi()
    venit_luna = get_raport_venituri(perioada='luna')
    stocuri_critice = verifica_stocuri_critice()
    lista_critica = ft.Column([
    ft.ListTile(
        title=ft.Text(p.nume_produs),
        subtitle=ft.Text(f"Stoc: {p.stoc_curent} (Minim: {p.stoc_minim})") 
    ) for p in stocuri_critice
])

    return ft.Column([
        ft.Text("Rapoarte și Analitice", size=30, weight="bold"),
        ft.Divider(),
        
        ft.Row([
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Vânzări Astăzi", size=16),
                        ft.Text(f"{venit_azi} RON", size=24, color="purple", weight="bold")
                    ]), padding=20
                )
            ),
            ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Vânzări Luna Aceasta", size=16),
                        ft.Text(f"{venit_luna} RON", size=24, color="purple", weight="bold")
                    ]), padding=20
                )
            ),
        ]),
        
        ft.Text("Alerte Stoc Critic", size=40, weight="bold", color="red"),
        lista_critica if stocuri_critice else ft.Text("Toate stocurile sunt în regulă.")
        
    ], scroll=ft.ScrollMode.AUTO, expand=True)