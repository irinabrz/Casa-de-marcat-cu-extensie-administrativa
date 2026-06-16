import flet as ft
from FUNCTII_SQL import get_lista_produse_completa, adauga_produs_nou, adauga_stoc_existent

def StocuriPage(page: ft.Page):
    from UI_DASHBOARD import DashboardPage

    page.controls.clear()
    page.update()

    def build_stock_table():
        produse = get_lista_produse_completa()
        rows = []
        for p in produse:
            culoare_stoc = "red200" if p['stoc_curent'] <= p['stoc_minim'] else "white"
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p['nume_produs'], color="white", weight="w500")),
                        ft.DataCell(ft.Text(p['categorie'], color="grey400")),
                        ft.DataCell(ft.Text(f"{float(p['pret']):.2f} RON", color="white")),
                        ft.DataCell(
                            ft.Row([
                                ft.Icon(ft.Icons.WARNING_ROUNDED, color="red200", size=16) if p['stoc_curent'] <= p['stoc_minim'] else ft.Icon(ft.Icons.CHECK_CIRCLE, color="green200", size=16),
                                ft.Text(str(p['stoc_curent']), color=culoare_stoc, weight="bold")
                            ], spacing=5)
                        ),
                    ]
                )
            )
        
        return ft.DataTable(
            heading_row_color="#1a1a24",
            divider_thickness=1,
            horizontal_lines=ft.BorderSide(1, "#22222a"),
            columns=[
                ft.DataColumn(ft.Text("Produs", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Categorie", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Preț (RON)", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Stoc Curent", color="pink200", weight="bold")),
            ],
            rows=rows,
        )
        
    tabel_container = ft.Column([build_stock_table()], scroll=ft.ScrollMode.AUTO)

    def refresh_data(e):
        tabel_container.controls.clear()
        tabel_container.controls.append(build_stock_table())
        page.update()

    btn_refresh = ft.IconButton(
        icon=ft.Icons.REFRESH_ROUNDED,
        icon_color="purple200",
        tooltip="Actualizează Datele",
        on_click=refresh_data
    )

    page.add(
        ft.Column([
            ft.TextButton(
                "Înapoi la Dashboard", 
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color="pink200",
                style=ft.ButtonStyle(color="pink200"),
                on_click=lambda _: [page.clean(), DashboardPage(page)]
            ),
            ft.Container(height=10),
            
            ft.Text("Gestiune Stocuri și Inventar", size=32, color="pink200", weight="bold"),
            ft.Text("Lista completă a produselor din cafenea și starea curentă a inventarului Oracle.", color="grey500", size=14),
            ft.Divider(height=40, color="#22222a"),
            
            ft.Row([
                ft.Text("Stocuri în Timp Real", size=18, weight="bold", color="white"),
                btn_refresh
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            
            ft.Container(
                content=tabel_container, 
                height=400, 
                bgcolor="#111115",
                border=ft.border.all(1, "#22222a"), 
                border_radius=14,
                padding=15
            ),
            
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )
    page.update()