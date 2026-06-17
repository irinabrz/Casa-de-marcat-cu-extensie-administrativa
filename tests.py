from django.test import TestCase
from django.utils import timezone
from django.db import IntegrityError
from datetime import timedelta
import oracledb
from LOGICA_DATABASE.models import Produs, Angajat, Cafenea, Client, Tranzactie, TranzactieProdus
from FUNCTII_SQL import (
    login_angajat_logic,
    cauta_client_dupa_nume,
    inregistreaza_client_nou,
    get_lista_produse_completa,
    get_toti_angajatii,
    adauga_produs_nou,
    verifica_stocuri_critice,
    calculeaza_vanzari_astazi,
    calculeaza_vanzari_saptamana,
    get_raport_venituri,
    get_istoric_comenzi,
    adauga_stoc_existent,
    date_grafic_venituri_pierderi,
    genereaza_date_raport_pdf,
    inregistreaza_vanzare,
    get_istoric_tranzactii_complet
)

class CafeneaSistemSuitaCompletaTests(TestCase):

    def setUp(self):
        """
        Această metodă rulează AUTOMAT înainte de FIECARE test individual.
        """
        self.cafenea = Cafenea.objects.create(nume_cafenea="MDS Testing Lab", adresa="Regie", oras="Bucuresti")
        self.angajat = Angajat.objects.create(cnp="1234567890123", nume_angajat="Popescu Irina", salariu=4500.00)
        
        self.produs_normal = Produs.objects.create(
            nume_produs="Espresso", pret=8.0, stoc_curent=50, stoc_minim=5, categorie="Cafea"
        )
        self.produs_critic = Produs.objects.create(
            nume_produs="Croissant", pret=7.5, stoc_curent=2, stoc_minim=10, categorie="Patiserie"
        )
        
        self.client = Client.objects.create(nume_client="Popa Andrei", nr_tranzactii=5)

    def test_01_conexiune_oracle_docker(self):
        """Verifică dacă containerul Oracle din Docker este pornit și răspunde."""
        try:
            conn = oracledb.connect(
                user="system", password="MDS_Cafenea_2026", dsn="localhost:1521/FREEPDB1"
            )
            self.assertIsNotNone(conn.version)
            conn.close()
        except Exception as e:
            self.fail(f"Baza de date Oracle din Docker nu este accesibilă! Eroare: {e}")

    def test_02_logic_login_angajat(self):
        """Testează funcția login_angajat_logic (Succes și Fail)."""
        rezultat_ok = login_angajat_logic("Popescu Irina")
        self.assertEqual(rezultat_ok["status"], "success")
        self.assertEqual(rezultat_ok["id"], self.angajat.id)
        rezultat_fail = login_angajat_logic("Nume Inexistent")
        self.assertEqual(rezultat_fail["status"], "error")
        self.assertIn("invalid", rezultat_fail["mesaj"])
    def test_03_cauta_si_inregistreaza_client(self):
        """Testează căutarea și crearea de clienți noi, inclusiv validările de duplicate."""
        client_gasit = cauta_client_dupa_nume("Iris Andreea")
        self.assertIsNotNone(client_gasit)
        self.assertEqual(client_gasit["nr_tranzactii"], 5)

        rezultat_nou = inregistreaza_client_nou("Andrei Noul Client")
        self.assertEqual(rezultat_nou["status"], "success")
        
        rezultat_duplicat = inregistreaza_client_nou("Popa Andrei")
        self.assertEqual(rezultat_duplicat["status"], "error")
        self.assertEqual(rezultat_duplicat["mesaj"], "Acest nume de client există deja")
    def test_04_verificare_si_adaugare_stocuri(self):
        """Testează detectarea produselor sub limita minimă și aprovizionarea."""
        critice = verifica_stocuri_critice()
        self.assertEqual(critice.count(), 1)
        self.assertEqual(critice.first().nume_produs, "Croissant")

        produs_actualizat = adauga_stoc_existent(self.produs_critic.id, cantitate_adaugata=20)
        self.assertEqual(produs_actualizat.stoc_curent, 22) 
        p_nou = adauga_produs_nou("Ceai Verde", 12.0, "Ceai", 30)
        self.assertIsNotNone(p_nou)
        self.assertEqual(Produs.objects.filter(nume_produs="Ceai Verde").count(), 1)

    def test_05_inregistreaza_vanzare_succes(self):
        """Vânzare normală: scade stocul, pune metoda de plată corectă și adaugă fidelitate clientului."""
        cos = [{'id': self.produs_normal.id, 'cantitate': 2}]
        
        t = inregistreaza_vanzare(
            id_angajat=self.angajat.id,
            lista_produse=cos,
            metoda_plata="Card",
            id_client=self.client.id
        )

        self.produs_normal.refresh_from_db()
        self.client.refresh_from_db()

        self.assertEqual(self.produs_normal.stoc_curent, 48)
        self.assertEqual(float(t.pret_total), 16.0)
        self.assertEqual(t.metoda_plata, "Card")
        self.assertEqual(self.client.nr_tranzactii, 6) 

    def test_06_inregistreaza_vanzare_stoc_insuficient(self):
        """Test critic de siguranță: Dacă se cere mai mult decât stocul, aruncă eroare și nu modifică nimic."""
        cos_exagerat = [{'id': self.produs_critic.id, 'cantitate': 500}]

        with self.assertRaises(Exception):
            inregistreaza_vanzare(
                id_angajat=self.angajat.id,
                lista_produse=cos_exagerat,
                metoda_plata="Cash"
            )

        self.produs_critic.refresh_from_db()
        self.assertEqual(self.produs_critic.stoc_curent, 2)


    def test_07_rapoarte_si_statistici_venituri(self):
        """Generează tranzacții fictive și testează acuratețea calculelor matematice pentru dashboard."""
        Tranzactie.objects.create(
            angajat=self.angajat, client=self.client, pret_total=100.0, 
            metoda_plata="Cash", data_tranzactie=timezone.now()
        )
        
        data_veche = timezone.now() - timedelta(days=4)
        Tranzactie.objects.create(
            angajat=self.angajat, client=self.client, pret_total=50.0, 
            metoda_plata="Card", data_tranzactie=data_veche
        )
        
        self.assertEqual(float(calculeaza_vanzari_astazi()), 100.0)
        self.assertEqual(float(calculeaza_vanzari_saptamana()), 150.0) 
        self.assertEqual(float(get_raport_venituri('luna')), 150.0)

        date_grafic = date_grafic_venituri_pierderi()
        self.assertTrue(len(date_grafic) > 0)

    def test_08_date_pdf_si_liste_flet(self):
        """Verifică structura de date trimisă către PDF-uri și tabelele din Flet."""
        t = Tranzactie.objects.create(angajat=self.angajat, pret_total=25.5, metoda_plata="Cash")
        TranzactieProdus.objects.create(tranzactie=t, produs=self.produs_normal, cantitate=1, pret_la_moment=8.0)

        date_pdf = genereaza_date_raport_pdf(t.id)
        self.assertEqual(date_pdf['tranzactie'].id, t.id)
        self.assertEqual(date_pdf['produse'].count(), 1)
        lista_produse_flet = get_lista_produse_completa()
        self.assertIsInstance(lista_produse_flet, list)
        self.assertEqual(len(lista_produse_flet), 2)
        self.assertIn("nume_produs", lista_produse_flet[0])
        istoric_tabel = get_istoric_tranzactii_complet()
        self.assertIsInstance(istoric_tabel, list)
        self.assertEqual(istoric_tabel[0]["angajat"], "Popescu Irina")