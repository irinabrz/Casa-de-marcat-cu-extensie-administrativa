# Design Patterns Folosite în Proiect

Acest document descrie pattern-urile de proiectare software identificate și aplicate în cadrul proiectului **Casa de Marcat cu Extensie Administrativă**.

---

## 1. MVC — Model-View-Controller

**Descriere:** Separarea aplicației în trei straturi distincte: date (Model), logică (Controller) și interfață (View).

**Cum apare în proiect:**

| Strat | Fișiere | Responsabilitate |
|---|---|---|
| **Model** | `LOGICA_DATABASE/models.py` | Definirea tabelelor: `Produs`, `Angajat`, `Client`, `Tranzactie` |
| **Controller** | `FUNCTII_SQL.py` | Logica de business: `inregistreaza_vanzare()`, calcul profit |
| **View** | `UI_VANZARE.py`, `UI_STOCURI.py`, `UI_RAPOARTE.py`, `UI_ISTORIC.py`, `UI_DASHBOARD.py` | Interfața grafică Flet afișată utilizatorului |

**Beneficiu:** Modificarea interfeței nu afectează logica de business și invers. Fiecare strat poate fi testat independent.

---

## 2. Separation of Concerns (Separarea Responsabilităților)

**Descriere:** Fiecare modul al aplicației are o singură responsabilitate clară și bine delimitată.

**Cum apare în proiect:**

- `agent_anomalii.py` — **exclusiv** detectarea tranzacțiilor suspecte cu AI
- `agent_predictiv_stoc.py` — **exclusiv** predicția epuizării stocului cu AI
- `FUNCTII_SQL.py` — **exclusiv** operațiile cu baza de date Oracle
- `CONFIG_SISTEM/` — **exclusiv** configurarea Django și a conexiunii la DB
- `LOGICA_DATABASE/` — **exclusiv** definirea modelelor (tabelelor) SQL

**Beneficiu:** Când apare o eroare legată de stoc, știi exact că trebuie să cauți în `UI_STOCURI.py` sau `agent_predictiv_stoc.py`, nu în tot proiectul.

---

## 3. Strategy Pattern

**Descriere:** Definirea unei familii de algoritmi care pot fi înlocuiți între ei fără a modifica codul care îi folosește.

**Cum apare în proiect:**

Cei doi agenți AI (`agent_anomalii.py` și `agent_predictiv_stoc.py`) sunt implementați ca module independente cu interfețe clare:

```python
# agent_anomalii.py
def verifica_anomalie_comanda(cantitate, valoare, tip_plata_id, istoric=None):
    # Strategia 1: IsolationForest
    ...

# agent_predictiv_stoc.py  
def estimeaza_zile_ramase_stoc_ai(id_produs):
    # Strategia 2: Linear Regression
    ...
```

Aceste funcții pot fi înlocuite cu algoritmi diferiți (ex: un model API extern, un alt clasificator) fără a modifica `UI_STOCURI.py` sau `UI_VANZARE.py` care le apelează.

**Beneficiu:** Flexibilitate în schimbarea algoritmului AI fără a afecta restul aplicației.

---

## 4. Facade Pattern

**Descriere:** O interfață simplificată peste un sistem complex.

**Cum apare în proiect:**

`FUNCTII_SQL.py` funcționează ca un **Facade** peste Django ORM și Oracle SQL. În loc ca UI-ul să scrie interogări complexe direct, apelează funcții simple:

```python
# În loc de interogări ORM complexe direct în UI:
from FUNCTII_SQL import inregistreaza_vanzare, adauga_produs_nou

# UI apelează simplu:
inregistreaza_vanzare(id_angajat=1, lista_produse=cos, metoda_plata="Cash")
```

**Beneficiu:** Codul din UI rămâne simplu și lizibil. Complexitatea SQL este ascunsă în spatele unor funcții cu nume clare.

---

## 5. Repository Pattern (prin Django ORM)

**Descriere:** Abstractizarea accesului la date printr-o interfață uniformă.

**Cum apare în proiect:**

Django ORM implementează automat acest pattern prin modelele definite în `LOGICA_DATABASE/models.py`. Accesul la date se face prin:

```python
# Nu scriem SQL raw, ci folosim Repository-ul Django:
Produs.objects.get(id=id_produs_curent)
Tranzactie.objects.filter(produs_id=id).order_by('data_creare')
```

**Beneficiu:** Dacă am schimba baza de date (de la Oracle la PostgreSQL), codul de business nu s-ar schimba deloc.

---

## Rezumat

| Pattern | Locație în cod | Beneficiu principal |
|---|---|---|
| MVC | `models.py` / `FUNCTII_SQL.py` / `UI_*.py` | Separare clară date-logică-interfață |
| Separation of Concerns | Toată structura proiectului | Ușurință în debugging și mentenanță |
| Strategy | `agent_anomalii.py`, `agent_predictiv_stoc.py` | Agenții AI pot fi înlocuiți independent |
| Facade | `FUNCTII_SQL.py` | UI simplu, SQL complex ascuns |
| Repository | `LOGICA_DATABASE/models.py` (Django ORM) | Independență față de tipul bazei de date |
