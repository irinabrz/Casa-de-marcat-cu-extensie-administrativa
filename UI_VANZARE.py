import flet as ft
from FUNCTII_SQL import get_lista_produse_completa

def VanzarePage(page: ft.Page):
    from UI_DASHBOARD import DashboardPage

    bon_curent = []

    def adauga_pe_bon(produs, cantitate, id_produs):
        """Adaugă produsul selectat în listă sau îi mărește cantitatea dacă există deja."""
        for item in bon_curent:
            if item["id"] == id_produs:
                item["cantitate"] += cantitate
                return
        
        nume = produs.nume_produs if hasattr(produs, 'nume_produs') else produs.get('nume_produs', 'Produs necunoscut')
        pret = float(produs.pret if hasattr(produs, 'pret') else produs.get('pret', 0.0))
        categorie = produs.categorie if hasattr(produs, 'categorie') else produs.get('categorie', '')
        
        bon_curent.append({
            "id": id_produs,
            "nume": nume,
            "pret": pret,
            "categorie": categorie,
            "cantitate": cantitate
        })

    def update_interfata_bon():
        """Actualizează lista vizuală a bonului și totalul de plată."""
        lista_vizuala_bon.controls.clear()
        total = 0.0
        
        for item in bon_curent:
            subtotal = item["pret"] * item["cantitate"]
            total += subtotal
            
            lista_vizuala_bon.controls.append(
                ft.ListTile(
                    leading=ft.Icon(get_icon_for_category(item["categorie"]), color="pink"),
                    title=ft.Text(f"{item['nume']} x {item['cantitate']}"),
                    subtitle=ft.Text(f"{item['pret']} RON/buc"),
                    trailing=ft.Text(f"{subtotal:.2f} RON", weight="bold"),
                )
            )
        
        text_total.value = f"Total: {total:.2f} RON"
        page.update()

    def deschide_dialog_cantitate(produs, nume_afisat, id_produs):
        """Deschide o fereastră pop-up care cere cantitatea pentru produsul selectat."""
        tf_cantitate = ft.TextField(value="1", keyboard_type=ft.KeyboardType.NUMBER, text_align=ft.TextAlign.CENTER, width=100)
        
        def confirma_adaugare(e):
            try:
                cant = int(tf_cantitate.value)
                if cant <= 0: raise ValueError()
                
                stoc_disponibil = produs.stoc_curent if hasattr(produs, 'stoc_curent') else produs.get('stoc_curent', 999)
                if cant > stoc_disponibil:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Stoc insuficient! Disponibil: {stoc_disponibil}"))
                    page.snack_bar.open = True
                    page.update()
                    return

                adauga_pe_bon(produs, cant, id_produs)
                dialog.open = False
                update_interfata_bon()
            except ValueError:
                tf_cantitate.error_text = "Introdu un număr valid!"
                page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Cantitate pentru {nume_afisat}"),
            content=ft.Row([
                ft.IconButton(ft.Icons.REMOVE, on_click=lambda _: [setattr(tf_cantitate, 'value', str(max(1, int(tf_cantitate.value) - 1))), page.update()]),
                tf_cantitate,
                ft.IconButton(ft.Icons.ADD, on_click=lambda _: [setattr(tf_cantitate, 'value', str(int(tf_cantitate.value) + 1)), page.update()]),
            ], alignment=ft.MainAxisAlignment.CENTER),
            actions=[
                ft.TextButton("Anulează", on_click=lambda _: [setattr(dialog, 'open', False), page.update()]),
                ft.ElevatedButton("Adaugă pe bon", bgcolor="pink", color="white", on_click=confirma_adaugare)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.overlay.append(dialog)
        dialog.open = True
        page.update()

    def afiseaza_alerta_predictiva_ui(lista_mesaje):
        """Deschide un dialog frumos în Flet când AI-ul prezice epuizarea stocului."""
        text_mesaje = "\n".join([f"• {m}" for m in lista_mesaje])
        
        def inchide(_):
            dialog_predictie.open = False
            page.update()

        dialog_predictie = ft.AlertDialog(
            title=ft.Text(" PROGNOZĂ EPUIZARE STOC (AI)", color="orange", weight="bold"),
            content=ft.Text(
                f"Sistemul de Machine Learning local a detectat o rată mare de consum:\n\n"
                f"{text_mesaje}\n\n"
                f"Se recomandă generarea unei note de aprovizionare în următoarele zile.",
                size=14
            ),
            actions=[ft.TextButton("Am înțeles", on_click=inchide)],
        )
        page.overlay.append(dialog_predictie)
        dialog_predictie.open = True
        page.update()

    def executa_salvare_oracle():
        """Scade produsele din Oracle și apoi apelează al doilea AI (Agent Predictiv Stoc)"""
        try:
            print("[DEBUG] Actualizare stocuri în Oracle și rulare prognoză AI...")
            produse_urgente_aprovizionare = []

            for item in bon_curent:
                id_produs = item["id"]
                cantitate_de_scazut = -int(item["cantitate"]) 
                
                from FUNCTII_SQL import adauga_stoc_existent
                from agent_predictiv_stoc import estimeaza_zile_ramase_stoc_ai 
                adauga_stoc_existent(id_produs, cantitate_de_scazut)
                
                se_termina, in_cate_zile, nume_p = estimeaza_zile_ramase_stoc_ai(id_produs)
                if se_termina:
                    produse_urgente_aprovizionare.append(f"{nume_p} (Se termină în aprox. {in_cate_zile} zile!)")
            
            page.snack_bar = ft.SnackBar(ft.Text("Vânzare salvată cu succes în Oracle!", color="white"), bgcolor="green")
            page.snack_bar.open = True
            
            bon_curent.clear()
            update_interfata_bon()

            if produse_urgente_aprovizionare:
                afiseaza_alerta_predictiva_ui(produse_urgente_aprovizionare)
            
        except Exception as ex:
            print(f"[ERROR Oracle Commit] {ex}")
            page.snack_bar = ft.SnackBar(ft.Text(f"Eroare critică la salvare: {ex}"))
            page.snack_bar.open = True
            page.update()

    def finalizeaza_comanda(e):
        """Funcția principală de checkout. Apelează primul AI (Agent Anomalii Tranzacționale)"""
        if not bon_curent:
            page.snack_bar = ft.SnackBar(ft.Text("Bonul este gol! Adaugă produse mai întâi."))
            page.snack_bar.open = True
            page.update()
            return
        
        print("[DEBUG] S-a apăsat Finalizare Comandă. Calculăm datele agregate...")
        
        cantitate_totala = sum(int(item["cantitate"]) for item in bon_curent)
        valoare_totala = sum(float(item["pret"]) * int(item["cantitate"]) for item in bon_curent)
        tip_plata_id = 1

        from FUNCTII_SQL import get_istoric_tranzactii_pentru_ai
        date_istorice_real = get_istoric_tranzactii_pentru_ai()

        este_anomalie = False

        try:
            from agent_anomalii import verifica_anomalie_comanda
            este_anomalie = verifica_anomalie_comanda(cantitate_totala, valoare_totala, tip_plata_id, date_istorice_real)
            print(f"[DEBUG] Rezultat evaluare Agent AI Anomalii -> este_anomalie: {este_anomalie}")
        except Exception as ai_ex:
            print(f"\n [EROARE AGENT AI ANOMALII]: {ai_ex}\n")
            este_anomalie = False  

        if este_anomalie:
            print("[DEBUG] Declanșare alertă vizuală anomalie. Blocare temporară directă SQL.")
            
            def inchide_dialog(_):
                dialog_alerta.open = False
                page.update()

            def forțează_salvarea(_):
                """Ignoră decizia agentului AI și trimite datele direct în Oracle SQL."""
                dialog_alerta.open = False
                page.update()
                print("[DEBUG] SUPRASCRIERE ADMINISTRATIVĂ: Operatorul a autorizat manual tranzacția.")
                executa_salvare_oracle()

            dialog_alerta = ft.AlertDialog(
                title=ft.Text(" ALERTĂ SECURITATE POS", color="red", weight="bold"),
                content=ft.Text(
                    f"Sistemul AI local a detectat o anomalie operațională/financiară!\n\n"
                    f"• Valoare totală calculată: {valoare_totala:.2f} RON\n"
                    f"• Volum produse pe bon: {cantitate_totala} bucăți\n\n"
                    f"Doriți să respingeți tranzacția sau să rulați o suprascriere manuală?",
                    size=15
                ),
                actions=[
                    ft.TextButton("Anulează și corectează", on_click=inchide_dialog),
                    ft.ElevatedButton("Forțează Finalizarea", bgcolor="red", color="white", on_click=forțează_salvarea)
                ],
                actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            
            page.overlay.append(dialog_alerta)
            dialog_alerta.open = True
            page.update()
            return 

        executa_salvare_oracle()

    def get_icon_for_category(categorie: str):
        """Returnează iconița corespunzătoare în funcție de numele categoriei."""
        if not categorie:
            return ft.Icons.FASTFOOD
        cat_low = str(categorie).lower()
        if "caf" in cat_low or "coffee" in cat_low:
            return ft.Icons.COFFEE
        elif "patis" in cat_low or "pake" in cat_low or "dulce" in cat_low or "desert" in cat_low or "bakery" in cat_low:
            return ft.Icons.CAKE
        else:
            return ft.Icons.FASTFOOD
    
    produse_db = get_lista_produse_completa()
    grid_produse = ft.GridView(expand=True, runs_count=3, max_extent=180, child_aspect_ratio=1.0, spacing=15, run_spacing=15)

    for p in produse_db:
        id_produs = p.id if hasattr(p, 'id') else p.get('id')
        nume_p = p.nume_produs if hasattr(p, 'nume_produs') else p.get('nume_produs', 'Fără Nume')
        pret_p = p.pret if hasattr(p, 'pret') else p.get('pret', 0.0)
        cat_p = p.categorie if hasattr(p, 'categorie') else p.get('categorie', '')
        
        iconita_categorie = get_icon_for_category(cat_p)
        card_produs = ft.ElevatedButton(
            content=ft.Container(
                content=ft.Column([
                    ft.Icon(iconita_categorie, color='white', size=45),
                    ft.Text(value=nume_p, color='white', size=14, text_align=ft.TextAlign.CENTER, weight="bold", max_lines=2),
                    ft.Text(value=f"{pret_p} RON", color='pink200', size=12)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                expand=True
            ),
            on_click=lambda _, prod=p, name=nume_p, id_p=id_produs: deschide_dialog_cantitate(prod, name, id_p),
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=10
            ),
            width=180,
            height=180,
        )
        grid_produse.controls.append(card_produs)

    lista_vizuala_bon = ft.ListView(expand=True, spacing=10)
    text_total = ft.Text("Total: 0.00 RON", size=22, weight="bold", color="pink")

    page.add(
        ft.Column([
            ft.ElevatedButton(
                "Înapoi la Dashboard", 
                icon=ft.Icons.ARROW_BACK,
                on_click=lambda _: [page.clean(), DashboardPage(page)]
            ),
            ft.Container(height=10),
            
            ft.Row([
                ft.Column([
                    ft.Text("Produse Disponibile", size=22, weight="bold"),
                    ft.Divider(),
                    ft.Container(content=grid_produse, expand=True)
                ], expand=3),
                
                ft.VerticalDivider(width=20),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("Bon Curent", size=22, weight="bold"),
                        ft.Divider(),
                        ft.Container(content=lista_vizuala_bon, expand=True),
                        ft.Divider(),
                        text_total,
                        ft.Container(height=10),
                        ft.ElevatedButton(
                            "FINALIZARE COMANDĂ", 
                            icon=ft.Icons.CHECK,
                            bgcolor="pink", 
                            color="white", 
                            width=300, 
                            height=50,
                            on_click=finalizeaza_comanda
                        )
                    ]),
                    padding=15,
                    bgcolor="#1e1e24",
                    border_radius=12,
                    expand=2
                )
            ], expand=True)
        ], expand=True)
    )
    page.update()