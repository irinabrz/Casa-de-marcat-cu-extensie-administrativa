import flet as ft
from FUNCTII_SQL import adauga_produs_nou, adauga_stoc_existent, get_lista_produse_completa

def MarfaNouaPage(page: ft.Page):
    def proceseaza_produs_nou(e):
        try:
            nume = nume_tf.value
            pret = float(pret_tf.value) if pret_tf.value else 0
            cat = cat_tf.value
            stoc = int(stoc_tf.value) if stoc_tf.value else 0
            adauga_produs_nou(nume, pret, cat, stoc)
            page.snack_bar = ft.SnackBar(ft.Text(f"Produsul '{nume}' a fost salvat!"))
            page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Eroare: {ex}"))
            page.snack_bar.open = True
        page.update()

    def proceseaza_update_stoc(e):
        try:
            if not dd_produse.value: return
            id_p = int(dd_produse.value)
            cant = int(cant_update_tf.value) if cant_update_tf.value else 0
            
            adauga_stoc_existent(id_p, cant)
            page.snack_bar = ft.SnackBar(ft.Text("Stoc actualizat cu succes!"))
            page.snack_bar.open = True
        except Exception as ex:
            page.snack_bar = ft.SnackBar(ft.Text(f"Eroare: {ex}"))
            page.snack_bar.open = True
        page.update()

    nume_tf = ft.TextField(label="Nume Produs Nou", border_color="pink")
    pret_tf = ft.TextField(label="Preț", keyboard_type=ft.KeyboardType.NUMBER)
    cat_tf = ft.TextField(label="Categorie")
    stoc_tf = ft.TextField(label="Stoc Inițial", value="0")
    
    produse = get_lista_produse_completa()
    dd_produse = ft.Dropdown(
        label="Alege produs existent",
        border_color="pink",
        options=[ft.dropdown.Option(key=str(p['id']), text=p['nume_produs']) for p in produse]
    )
    cant_update_tf = ft.TextField(label="Cantitate primită", value="0")

    return ft.Column([
        ft.Text("GESTIUNE INTRARE MARFĂ", size=28, weight="bold"),
        ft.Divider(height=20),
        
        ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Text("Adăugare Produs NOU", size=18, weight="bold", color="pink"),
                    nume_tf, pret_tf, cat_tf, stoc_tf,
                    ft.ElevatedButton("Salvează Produs Nou", on_click=proceseaza_produs_nou, bgcolor="pink", color="white", width=300)
                ], spacing=15),
                padding=20, 
                border=ft.border.all(2, "pink200"), 
                border_radius=15,
                expand=True
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(" Reaprovizionare Stoc", size=18, weight="bold", color="magenta"),
                    dd_produse, 
                    cant_update_tf,
                    ft.Text("(Selectează produsul și adaugă cantitatea primită)", size=12, italic=True),
                    ft.ElevatedButton("Actualizează Stoc", on_click=proceseaza_update_stoc, bgcolor="pink", color="white", width=300)
                ], spacing=15),
                padding=20, 
                border=ft.border.all(2, "pink200"), 
                border_radius=15,
                expand=True
            ),
        ], 
        alignment=ft.MainAxisAlignment.START, 
        vertical_alignment=ft.CrossAxisAlignment.START,
        spacing=20)
    ], scroll=ft.ScrollMode.ALWAYS, expand=True)