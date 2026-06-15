"""
💾 SCHEMA BAZEI DE DATE (Django Models)
Scop: Definește tabelele 'Produs' și 'Comanda' în Oracle SQL.
Instrucțiuni: După modificare, rulați 'makemigrations' și 'migrate'.
"""
from django.db import models

class Cafenea(models.Model):
    nume_cafenea = models.CharField(max_length=100)
    adresa = models.CharField(max_length=200)
    oras = models.CharField(max_length=50)

class Angajat(models.Model):
    nume_angajat = models.CharField(max_length=100)
    salariu = models.DecimalField(max_digits=10, decimal_places=2)
    cnp = models.CharField(max_length=13, unique=True)

class Produs(models.Model):
    nume_produs = models.CharField(max_length=100)
    pret = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.CharField(max_length=50)
    stoc_curent = models.IntegerField(default=0)
    stoc_minim = models.IntegerField(default=5)
    def __str__(self):
        return f"{self.nume_produs} - {self.pret} RON (Stoc: {self.stoc_curent})"

class Client(models.Model):
    nume_client = models.CharField(max_length=100)
    nr_tranzactii = models.IntegerField(default=0)

class Tranzactie(models.Model):
    client = models.ForeignKey(Client, on_delete=models.SET_NULL, null=True)
    angajat = models.ForeignKey(Angajat, on_delete=models.CASCADE)
    pret_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_tranzactie = models.DateTimeField(auto_now_add=True)
    metoda_plata = models.CharField(max_length=20)

class TranzactieProdus(models.Model):
    produs = models.ForeignKey(Produs, on_delete=models.CASCADE)
    tranzactie = models.ForeignKey(Tranzactie, on_delete=models.CASCADE)
    cantitate = models.IntegerField(default=1)
    pret_la_moment = models.DecimalField(max_digits=10, decimal_places=2)