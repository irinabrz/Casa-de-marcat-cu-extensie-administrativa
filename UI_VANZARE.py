import flet as ft

def VanzarePage(page: ft.Page, gestiune):
    tabel_bon = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Produs")),
            ft.DataColumn(ft.Text("Preț")),
            ft.DataColumn(ft.Text("Acțiuni")),
        ]
    )

    def AdaugaProdus(e):
        cod_introdus = field_cod.value
        produs_gasit = next((p for p in gestiune.lista_produse if p.cod == cod_introdus), None)

        if produs_gasit:
            tabel_bon.rows.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(produs_gasit.nume)),
                    ft.DataCell(ft.Text(str(produs_gasit.pret))),
                    ft.DataCell(ft.IconButton(ft.icons.DELETE, on_click=lambda _: print("Sterge")))
                ])
            )
            field_cod.value = ""
            page.update()
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Produsul nu a fost găsit în stoc!"))
            page.snack_bar.open = True
            page.update()

    field_cod = ft.TextField(label="Scanează Cod Produs", on_submit=adauga_produs)
    
    return ft.Column([
        ft.Text("Terminal Vânzări", size=30, weight="bold"),
        ft.Row([field_cod, ft.ElevatedButton("Adaugă", on_click=adauga_produs)]),
        tabel_bon
    ])
