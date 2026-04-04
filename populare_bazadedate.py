import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CONFIG_SISTEM.settings')
django.setup()

from LOGICA_DATABASE.models import Produs, Angajat, Client, Tranzactie, Cafenea

def populare():
    print(" Incepem popularea bazei de date Oracle cu noile modele...")

    try:
        cafenea, _ = Cafenea.objects.get_or_create(
            nume_cafenea="MDS Coffee Lab", 
            adresa="Strada Academiei 1", 
            oras="Bucuresti"
        )

        angajat, _ = Angajat.objects.get_or_create(
            cnp="1234567890123", 
            defaults={'nume_angajat': "Popescu Irina", 'salariu': 4500.00}
        )
        produse = [
            {"nume": "Espresso Short", "pret": 8.0, "stoc": 100, "cat": "Cafea"},
            {"nume": "Cafea Lunga", "pret": 10.5, "stoc": 80, "cat": "Cafea"},
            {"nume": "Croissant", "pret": 7.5, "stoc": 20, "cat": "Patiserie"},
        ]

        for p in produse:
            Produs.objects.get_or_create(
                nume_produs=p["nume"],
                defaults={'pret': p["pret"], 'stoc_curent': p["stoc"], 'categorie': p["cat"]}
            )
        
        print(" Populare reușită în Oracle!")

    except Exception as e:
        print(f"Eroare la populare: {e}")

if __name__ == "__main__":
    populare()