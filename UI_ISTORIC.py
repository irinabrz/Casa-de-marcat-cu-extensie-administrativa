import flet as ft
from FUNCTII_SQL import get_istoric_tranzactii_complet

def IstoricTranzactiiPage(page: ft.Page):
    from UI_DASHBOARD import DashboardPage

    page.controls.clear()
    page.update()

    def build_history_table():
        tranzactii = get_istoric_tranzactii_complet()
        rows = []
        
        for t in tranzactii:
            # Alegem o iconiță diferită în funcție de metoda de plată
            iconita_plata = ft.Icons.MONEY_ROUNDED if str(t['metoda']).lower() == 'cash' else ft.Icons.CREDIT_CARD_ROUNDED
            color_plata = "green200" if str(t['metoda']).lower() == 'cash' else "purple200"

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(f"#{t['id']}", color="pink200", weight="bold")),
                        ft.DataCell(ft.Text(str(t['data']), color="white")),
                        ft.DataCell(ft.Text(str(t['angajat']), color="grey400")),
                        ft.DataCell(
                            ft.Row([
                                ft.Icon(iconita_plata, color=color_plata, size=16),
                                ft.Text(str(t['metoda']), color="white")
                            ], spacing=5)
                        ),
                        ft.DataCell(ft.Text(f"{float(t['total']):.2f} RON", color="white", weight="w600")),
                    ]
                )
            )
        
        return ft.DataTable(
            heading_row_color="#1a1a24",
            divider_thickness=1,
            horizontal_lines=ft.BorderSide(1, "#22222a"),
            columns=[
                ft.DataColumn(ft.Text("ID", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Dată & Oră", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Angajat", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Metodă Plată", color="pink200", weight="bold")),
                ft.DataColumn(ft.Text("Total Încasat", color="pink200", weight="bold")),
            ],
            rows=rows,
        )

    tabel_container = ft.Column([build_history_table()], scroll=ft.ScrollMode.AUTO)

    def refresh_data(e):
        tabel_container.controls.clear()
        tabel_container.controls.append(build_history_table())
        page.update()

    btn_refresh = ft.IconButton(
        icon=ft.Icons.REFRESH_ROUNDED,
        icon_color="purple200",
        tooltip="Reîmprospătează Istoricul",
        on_click=refresh_data
    )

    page.add(
        ft.Column([
            # Butonul Înapoi asortat
            ft.TextButton(
                "Înapoi la Dashboard", 
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color="pink200",
                style=ft.ButtonStyle(color="pink200"),
                on_click=lambda _: [page.clean(), DashboardPage(page)]
            ),
            ft.Container(height=10),
            
            # Header
            ft.Text("Istoric Tranzacții", size=32, color="pink200", weight="bold"),
            ft.Text("Vizualizează și urmărește toate bonurile fiscale emise prin casa de marcat locală.", color="grey500", size=14),
            ft.Divider(height=40, color="#22222a"),
            
            # Sub-header
            ft.Row([
                ft.Text("Toate vânzările înregistrate", size=18, weight="bold", color="white"),
                btn_refresh
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=10),
            
            # Tabelul încadrat în containerul întunecat
            ft.Container(
                content=tabel_container, 
                height=450, 
                bgcolor="#111115",
                border=ft.border.all(1, "#22222a"), 
                border_radius=14,
                padding=15
            ),
            
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    )
    page.update()