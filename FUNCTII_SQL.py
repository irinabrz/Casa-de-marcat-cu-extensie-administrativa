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


def adauga_produs_nou(nume, pret, cat, stoc):
    try:
        p = Produs.objects.create(nume_produs=nume, pret=pret, categorie=cat, stoc_curent=stoc)
        return p
    except IntegrityError:
        return None

def verifica_stocuri_critice():
    """Returnează produsele care au stocul sub limita minimă."""
    return Produs.objects.filter(stoc_curent__lt=models.F('stoc_minim'))
def calculeaza_vanzari_astazi():
    azi = timezone.now().date()
    total = Tranzactie.objects.filter(data_tranzactie__date=azi).aggregate(Sum('pret_total'))['pret_total__sum']
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
def inregistreaza_vanzare(id_angajat, lista_produse, metoda_plata, id_client=None):
    """
    id_angajat: int
    lista_produse: lista de dictionare [{'id': 1, 'cantitate': 2}, ...]
    """
    total_bon = 0
    angajat = Angajat.objects.get(id=id_angajat)
    client = Client.objects.get(id=id_client) if id_client else None

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

