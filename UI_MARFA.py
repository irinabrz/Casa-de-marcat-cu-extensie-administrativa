import flet as ft
from FUNCTII_SQL import adauga_produs_nou, adauga_stoc_existent, get_lista_produse_completa

def MarfaNouaPage(page: ft.Page):
    from UI_DASHBOARD import DashboardPage
    page.controls.clear()
    page.update()

    def proceseaza_produs_nou(e):
        try:
            nume = nume_tf.value
            pret = float(pret_tf.value) if pret_tf.value else 0
            cat = cat_tf.value
            stoc = int(stoc_tf.value) if stoc_tf.value else 0
            adauga_produs_nou(nume, pret, cat, stoc)
            page.snack_bar = ft.SnackBar(ft.Text(f"Produsul '{nume}' a fost salvat!"), bgcolor="green700")
            page.snack_bar.open = True
            nume_tf.value = ""
            pret_tf.value = ""
            cat_tf.value = ""
            stoc_tf.value = "0"
            MarfaNouaPage(page)
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Eroare: {ex}"), bgcolor="red700")
            page.snack_bar.open = True
        page.update()

    def proceseaza_update_stoc(e):
        try:
            if not dd_produse.value: return
            id_p = int(dd_produse.value)
            cant = int(cant_update_tf.value) if cant_update_tf.value else 0
            adauga_stoc_existent(id_p, cant)
            page.snack_bar = ft.SnackBar(ft.Text("Stoc actualizat cu succes!"), bgcolor="green700")
            page.snack_bar.open = True
            cant_update_tf.value = "0"
            page.update()
            
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Eroare: {ex}"), bgcolor="red700")
            page.snack_bar.open = True
        page.update()

    nume_tf = ft.TextField(label="Nume Produs Nou", border_color="#3e3e4a", focused_border_color="purple200", label_style=ft.TextStyle(color="grey400"))
    pret_tf = ft.TextField(label="Preț", keyboard_type=ft.KeyboardType.NUMBER, border_color="#3e3e4a", focused_border_color="purple200", label_style=ft.TextStyle(color="grey400"))
    cat_tf = ft.TextField(label="Categorie", border_color="#3e3e4a", focused_border_color="purple200", label_style=ft.TextStyle(color="grey400"))
    stoc_tf = ft.TextField(label="Stoc Inițial", value="0", keyboard_type=ft.KeyboardType.NUMBER, border_color="#3e3e4a", focused_border_color="purple200", label_style=ft.TextStyle(color="grey400"))
    
    produse = get_lista_produse_completa()
    dd_produse = ft.Dropdown(
        label="Alege produs existent",
        border_color="#3e3e4a",
        focused_border_color="purple200",
        label_style=ft.TextStyle(color="grey400"),
        options=[ft.dropdown.Option(key=str(p['id']), text=p['nume_produs']) for p in produse]
    )
    cant_update_tf = ft.TextField(label="Cantitate primită", value="0", keyboard_type=ft.KeyboardType.NUMBER, border_color="#3e3e4a", focused_border_color="purple200", label_style=ft.TextStyle(color="grey400"))

    page.add(
        ft.Column([
            ft.TextButton(
                "Înapoi la Dashboard", 
                icon=ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                icon_color="purple200",
                style=ft.ButtonStyle(color="purple200"),
                on_click=lambda _: [page.clean(), DashboardPage(page)]
            ),
            ft.Container(height=10),
            
            ft.Text("GESTIUNE INTRARE MARFĂ", size=30, color="pink200", weight="bold"),
            ft.Text("Înregistrarea produselor noi și recepția stocurilor în baza de date Oracle.", color="grey500", size=14),
            ft.Divider(height=30, color="#22222a"),
            
            ft.Row([
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ADD_BOX_ROUNDED, color="purple200", size=22),
                            ft.Text("Adăugare Produs NOU", size=18, weight="bold", color="white"),
                        ], spacing=10),
                        ft.Container(height=5),
                        
                        nume_tf, pret_tf, cat_tf, stoc_tf,
                        
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            content=ft.Text("Salvează Produs Nou", weight="bold"),
                            on_click=proceseaza_produs_nou, 
                            bgcolor="purple200", 
                            color="black", 
                            width=300,
                            height=45,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ], spacing=15),
                    bgcolor="#111115",
                    padding=25, 
                    border=ft.border.all(1, "#22222a"), 
                    border_radius=14,
                    expand=True
                ),
                
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.REPLAY_ROUNDED, color="purple200", size=22),
                            ft.Text("Reaprovizionare Stoc", size=18, weight="bold", color="white"),
                        ], spacing=10),
                        ft.Container(height=5),
                        
                        dd_produse, 
                        cant_update_tf,
                        ft.Text("(Selectează produsul și adăugă cantitatea primită)", size=12, italic=True, color="grey600"),
                        
                        ft.Container(height=53),
                        ft.ElevatedButton(
                            content=ft.Text("Actualizează Stoc", weight="bold"),
                            on_click=proceseaza_update_stoc, 
                            bgcolor="purple200", 
                            color="black", 
                            width=300,
                            height=45,
                            style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                        )
                    ], spacing=15),
                    bgcolor="#111115",
                    padding=25, 
                    border=ft.border.all(1, "#22222a"), 
                    border_radius=14,
                    expand=True
                ),
            ], 
            alignment=ft.MainAxisAlignment.START, 
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=20)
        ], scroll=ft.ScrollMode.ALWAYS, expand=True)
    )
    page.update()