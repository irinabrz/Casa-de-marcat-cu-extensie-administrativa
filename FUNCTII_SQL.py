"""LOGICĂ CALCULE (SQL Queries)
Scop: Funcții care extrag date din Oracle pentru rapoarte (Profit zilnic/lunar).
"""
from django.db import models, transaction
from LOGICA_DATABASE.models import Produs, Tranzactie, TranzactieProdus, Client, Angajat
from django.utils import timezone
from django.db.models import Sum
from datetime import timedelta
from django.db import IntegrityError
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from fpdf import FPDF

def login_angajat_logic(nume_angajat):
    """Verifică existența angajatului pentru identificarea la casă."""
    angajat = Angajat.objects.filter(nume_angajat=nume_angajat).first()
    if angajat:
        return {"status": "success", "id": angajat.id, "nume": angajat.nume_angajat}
    return {"status": "error", "mesaj": "Nume de angajat invalid"}

def cauta_client_dupa_nume(nume_client):
    """Caută un client și returnează datele lui pentru fidelizare."""
    client = Client.objects.filter(nume_client=nume_client).first()
    if client:
        return {
            "id": client.id, 
            "nume": client.nume_client, 
            "nr_tranzactii": client.nr_tranzactii
        }
    return None

def inregistreaza_client_nou(nume_client):
    """Creează un client nou cu validările necesare."""
    if not nume_client:
        return {"status": "error", "mesaj": "Numele este obligatoriu"}
        
    if Client.objects.filter(nume_client=nume_client).exists():
        return {"status": "error", "mesaj": "Acest nume de client există deja"}
        
    client_nou = Client.objects.create(nume_client=nume_client)
    return {"status": "success", "id": client_nou.id}
def get_istoric_tranzactii_pentru_ai():
    """
    Extrage dinamic istoricul tuturor vânzărilor din baza de date Oracle 
    folosind infrastructura Django ORM pentru a alimenta modelul AI.
    """
    try:
        from LOGICA_DATABASE.models import Tranzactie
        toate_tranzactiile = Tranzactie.objects.all()
        
        if toate_tranzactiile.exists():
            istoric = []
            for t in toate_tranzactiile:
                cantitate = int(t.cantitate) if hasattr(t, 'cantitate') else 1
                total = float(t.pret_total) if hasattr(t, 'pret_total') else float(t.total)
                
                istoric.append([cantitate, total, 1])
            return istoric
            
        return []
    except Exception as e:
        print(f"[ DB ERROR] Nu s-a putut genera istoricul pentru AI: {e}")
        return []
def get_lista_produse_completa():
    """Returnează toate produsele sub formă de listă de dicționare pentru tabelele Flet."""
    return list(Produs.objects.all().values(
        "id", "nume_produs", "pret", "categorie", "stoc_curent", "stoc_minim"
    ))

def get_toti_angajatii():
    """Returnează lista angajaților pentru dropdown-ul de selecție din Flet."""
    return list(Angajat.objects.all().values('id', 'nume_angajat'))

def adauga_produs_nou(nume, pret, cat, stoc):
    try:
        p = Produs.objects.create(nume_produs=nume, pret=pret, categorie=cat, stoc_curent=stoc)
        return p
    except IntegrityError:
        return None
import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

def estimeaza_zile_ramase_stoc_ai(id_produs_curent):
    """
    Analizează istoricul vânzărilor din Oracle pentru un produs și estimează 
    în câte zile stocul va ajunge la 0 folosind Regresie Liniară.
    """
    try:
        from LOGICA_DATABASE.models import Produs, Tranzactie
        
        produs = Produs.objects.get(id=id_produs_curent)
        stoc_actual = int(produs.stoc_curent)
        
        if stoc_actual <= 0:
            return True, 0, produs.nume_produs
        vonzari = Tranzactie.objects.filter(produs_id=id_produs_curent).order_by('data_creare')
        
        if vonzari.count() < 3:
            if stoc_actual < 5:
                return True, 1, produs.nume_produs
            return False, 999, ...

        X_zile = []
        Y_stoc_istoric = []
        
        
        prima_data = vonzari.first().data_creare
        stoc_calculat = stoc_actual
        
        for v in vonzari:
            diferenta_zile = (v.data_creare - prima_data).days
            X_zile.append([diferenta_zile])
            stoc_calculat += v.cantitate
            Y_stoc_istoric.append(stoc_calculat)
            
        X = np.array(X_zile)
        y = np.array(Y_stoc_istoric)
        
        model = LinearRegression()
        model.fit(X, y)
        
        rata_vanzare_pe_zi = model.coef_[0]
        
        if rata_vanzare_pe_zi >= 0:
            return False, 999, produs.nume_produs
            
        zile_ramase = - (stoc_actual) / rata_vanzare_pe_zi
        
        PRAG_SIGURANTA_ZILE = 3
        if zile_ramase <= PRAG_SIGURANTA_ZILE:
            return True, round(zile_ramase, 1), produs.nume_produs
            
        return False, round(zile_ramase, 1), produs.nume_produs
        
    except Exception as e:
        print(f"[ AI PREDICT ERROR] {e}")
        return False, 999, ""
def verifica_stocuri_critice():
    """Returnează produsele care au stocul sub limita minimă."""
    return Produs.objects.filter(stoc_curent__lt=models.F('stoc_minim'))
def calculeaza_vanzari_astazi():
    acum = timezone.now()
    start_azi = acum.replace(hour=0, minute=0, second=0, microsecond=0)
    total = Tranzactie.objects.filter(data_tranzactie__gte=start_azi).aggregate(Sum('pret_total'))['pret_total__sum']
    return total or 0
def calculeaza_vanzari_saptamana():
    """Calculează suma totală a vânzărilor din ultimele 7 zile."""
    acum = timezone.now()
    start_saptamana = acum - timedelta(days=7)
    total = Tranzactie.objects.filter(data_tranzactie__gte=start_saptamana).aggregate(Sum('pret_total'))['pret_total__sum']
    return total or 0
def get_raport_venituri(perioada='zi'):
    """Calculează suma totală încasată pe diferite perioade."""
    acum = timezone.now()
    if perioada == 'zi':
        start = acum.replace(hour=0, minute=0, second=0)
    elif perioada == 'saptamana':
        start = acum - timedelta(days=7)
    elif perioada == 'luna':
        start = acum - timedelta(days=30)
    
    total = Tranzactie.objects.filter(data_tranzactie__gte=start).aggregate(Sum('pret_total'))['pret_total__sum']
    return total or 0
def get_istoric_comenzi(data_start=None, data_end=None):
    """Returnează tranzacțiile. Dacă primește date, filtrează între ele."""
    comenzi = Tranzactie.objects.all().order_by('-data_tranzactie')
    if data_start and data_end:
        comenzi = comenzi.filter(data_tranzactie__date__range=[data_start, data_end])
    return comenzi
def adauga_stoc_existent(id_produs, cantitate_adaugata):
    """Actualizează stocul când se cumpără marfă nouă (achiziție)."""
    p = Produs.objects.get(id=id_produs)
    p.stoc_curent += cantitate_adaugata
    p.save()
    return p
def date_grafic_venituri_pierderi():
    """Pregătește datele pentru grafice (Venituri din vânzări)."""
    sapte_zile_ago = timezone.now().date() - timedelta(days=7)
    date_venituri = (
        Tranzactie.objects.filter(data_tranzactie__date__gte=sapte_zile_ago)
        .annotate(ziua=TruncDay('data_tranzactie'))
        .values('ziua')
        .annotate(total=Sum('pret_total'))
        .order_by('ziua')
    )
    return list(date_venituri)
def genereaza_date_raport_pdf(id_tranzactie):
    """Extrage toate datele unei comenzi pentru a fi trimise către generatorul de PDF."""
    t = Tranzactie.objects.get(id=id_tranzactie)
    detalii = TranzactieProdus.objects.filter(tranzactie=t)
    return {
        'tranzactie': t,
        'produse': detalii
    }
@transaction.atomic
def inregistreaza_vanzare(id_angajat, lista_produse, metoda_plata, nume_client_str=None):
    """
    id_angajat: int
    lista_produse: lista de dictionare [{'id': 1, 'cantitate': 2}, ...]
    nume_client_str: str (Numele preluat direct din TextField-ul din Flet)
    """
    total_bon = 0
    angajat = Angajat.objects.get(id=id_angajat)
    
    client = None
    if nume_client_str and nume_client_str.strip():
        nume_curat = nume_client_str.strip()
        client = Client.objects.filter(nume_client=nume_curat).first()
        if not client:
            client = Client.objects.create(nume_client=nume_curat)

    t = Tranzactie.objects.create(angajat=angajat, client=client, metoda_plata=metoda_plata)
    
    for item in lista_produse:
        p = Produs.objects.get(id=item['id'])
        
        if p.stoc_curent < item['cantitate']:
            raise Exception(f"Stoc insuficient pentru {p.nume_produs}")
            
        TranzactieProdus.objects.create(
            tranzactie=t,
            produs=p,
            cantitate=item['cantitate'],
            pret_la_moment=p.pret
        )
        p.stoc_curent -= item['cantitate']
        p.save()
        total_bon += (p.pret * item['cantitate'])
        
    t.pret_total = total_bon
    t.save()
    
    if client:
        client.nr_tranzactii += 1
        client.save()
        
    return t
def get_istoric_tranzactii_complet():
    """
    Extrage toate tranzacțiile din Oracle prin Django ORM ordonate descrescător 
    după dată și le returnează mapate frumos sub formă de dicționare pentru UI_ISTORIC.py.
    """
    try:
        tranzactii = Tranzactie.objects.all().select_related('angajat').order_by('-data_tranzactie')
        rezultat = []
        
        for t in tranzactii:
            data_str = t.data_tranzactie.strftime("%Y-%m-%d %H:%M") if hasattr(t, 'data_tranzactie') and t.data_tranzactie else "N/A"
            nume_angajat = t.angajat.nume_angajat if t.angajat else "Sistem"
            total_plata = float(t.pret_total) if hasattr(t, 'pret_total') else 0.0
            
            rezultat.append({
                "id": t.id,
                "data": data_str,
                "angajat": nume_angajat,
                "metoda": t.metoda_plata if hasattr(t, 'metoda_plata') else "Cash",
                "total": total_plata
            })
        return rezultat
    except Exception as e:
        print(f"[DB ERROR Istoric] Nu s-au putut prelua tranzacțiile: {e}")
        return []
    
def generare_bon_fiscal(id_tranzactie, calePDF = "bon_fiscal.pdf"):
    
    date_raport = genereaza_date_raport_pdf(id_tranzactie)
    tranzactie = date_raport['tranzactie']
    produse = date_raport['produse']

    
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.add_page()
    
    
    font_familie = "Arial"
    pdf.set_font(font_familie, style="B", size=16)
    
    
    pdf.cell(0, 10, txt=f"RAPORT TRANZACTIE #{tranzactie.id}", ln=True, align="C")
    pdf.ln(5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)

    
    pdf.set_font(font_familie, style="", size=11)
    data_formatata = tranzactie.data_tranzactie.strftime('%d-%m-%Y %H:%M') if tranzactie.data_tranzactie else "N/A"
    
    pdf.cell(40, 7, txt="Data Tranzactie:")
    pdf.cell(0, 7, txt=data_formatata, ln=True)
    if tranzactie.client:
        nume_client = getattr(tranzactie.client, 'nume_client', 'Client Anonim')
    else:
        nume_client = "Client Anonim"   
    pdf.cell(40, 7, txt="Client:")
    pdf.cell(0, 7, txt=nume_client, ln=True)
    pdf.ln(10)

    
    col_produs, col_cantitate, col_pret_unitar, col_total = 85, 25, 40, 40
    
    
    pdf.set_font(font_familie, style="B", size=11)
    pdf.set_fill_color(240, 240, 240)
    pdf.cell(col_produs, 10, "Denumire Produs", border=1, fill=True)
    pdf.cell(col_cantitate, 10, "Cantitate", border=1, align="C", fill=True)
    pdf.cell(col_pret_unitar, 10, "Pret Unitar", border=1, align="R", fill=True)
    pdf.cell(col_total, 10, "Total", border=1, align="R", ln=True, fill=True)

    
    pdf.set_font(font_familie, style="", size=10)
    for item in produse:
        nume_p = item.produs.nume_produs if hasattr(item, 'produs') else "Produs"
        cantitate_p = item.cantitate
        pret_u = float(item.pret_la_moment)
        pret_t = pret_u * cantitate_p

        pdf.cell(col_produs, 8, txt=str(nume_p), border=1)
        pdf.cell(col_cantitate, 8, txt=str(cantitate_p), border=1, align="C")
        pdf.cell(col_pret_unitar, 8, txt=f"{pret_u:.2f} LEI", border=1, align="R")
        pdf.cell(col_total, 8, txt=f"{pret_t:.2f} LEI", border=1, align="R", ln=True)

    
    pdf.ln(5)
    pdf.set_font(font_familie, style="B", size=12)
    pdf.cell(col_produs + col_cantitate + col_pret_unitar, 10, txt="TOTAL GENERAL:", align="R")
    valoare_totala = float(tranzactie.pret_total)
    pdf.cell(col_total, 10, txt=f"{valoare_totala:.2f} LEI", border=1, align="R", ln=True)

    
    pdf.output(calePDF)
    
    return calePDF