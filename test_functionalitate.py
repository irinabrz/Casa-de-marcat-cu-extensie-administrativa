import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONFIG_SISTEM.settings')
django.setup()

from LOGICA_DATABASE.models import Produs, Angajat, Client, Tranzactie
from FUNCTII_SQL import inregistreaza_vanzare, adauga_produs_nou

def test_proces_vanzare_complet():
    print("\n--- START TEST AUTOMAT ---")
    
    try:
        angajat = Angajat.objects.first()
        produs = Produs.objects.filter(nume_produs="Cafea Lunga").first()
        
        if not angajat or not produs:
            print(" Eroare: Nu am găsit angajatul sau produsul în bază!")
            return

        stoc_initial = produs.stoc_curent
        print(f"Stoc înainte de vânzare: {stoc_initial}")

        cos = [{'id': produs.id, 'cantitate': 1}]
        tranzactie = inregistreaza_vanzare(
            id_angajat=angajat.id, 
            lista_produse=cos, 
            metoda_plata="Cash"
        )

        produs.refresh_from_db()
        
        if produs.stoc_curent == stoc_initial - 1:
            print(f" SUCCES: Stocul a scăzut corect ({produs.stoc_curent})")
        else:
            print(f"FAIL: Stocul nu a scăzut corect! (Actual: {produs.stoc_curent})")

        if tranzactie.pret_total == produs.pret:
            print(f"SUCCES: Prețul total este corect ({tranzactie.pret_total} RON)")

    except Exception as e:
        print(f"EROARE CRITICĂ: {e}")

if __name__ == "__main__":
    test_proces_vanzare_complet()