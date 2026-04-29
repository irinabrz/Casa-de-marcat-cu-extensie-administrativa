import flet as ft
from FUNCTII_SQL import get_lista_produse_completa, adauga_produs_nou, adauga_stoc_existent

def StocuriPage(page: ft.Page):
    def build_stock_table():
        produse = get_lista_produse_completa()
        rows = []
        for p in produse:
            culoare_stoc = "red" if p['stoc_curent'] <= p['stoc_minim'] else "black"
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p['nume_produs'])),
                        ft.DataCell(ft.Text(p['categorie'])),
                        ft.DataCell(ft.Text(str(p['pret']))),
                        ft.DataCell(ft.Text(str(p['stoc_curent']), color=culoare_stoc, weight="bold")),
                    ]
                )
            )
        
        return ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Produs")),
                ft.DataColumn(ft.Text("Categorie")),
                ft.DataColumn(ft.Text("Preț (RON)")),
                ft.DataColumn(ft.Text("Stoc Curent")),
            ],
            rows=rows,
        )
    tabel_container = ft.Column([build_stock_table()], scroll=ft.ScrollMode.AUTO)

    def refresh_data(e):
        tabel_container.controls.clear()
        tabel_container.controls.append(build_stock_table())
        page.update()

    btn_refresh = ft.ElevatedButton("Actualizează Tabel Stocuri", on_click=refresh_data, color="orange")
    return ft.Column([
        ft.Text("Gestiune Stocuri și Inventar", size=25, weight="bold"),
        ft.Divider(),
        ft.Text("Stocuri în Timp Real:", size=22, weight="bold", color="black"),
        btn_refresh,
        ft.Container(content=tabel_container, height=300, border=ft.border.all(1, "grey300"), border_radius=10),
        
        ft.Divider(),
    ], scroll=ft.ScrollMode.AUTO)