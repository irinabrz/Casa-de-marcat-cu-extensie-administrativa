# Raport: Utilizarea Instrumentelor AI în Procesul de Dezvoltare

## Introducere

Pe parcursul dezvoltării acestui proiect (**Casa de Marcat cu Extensie Administrativă**) am folosit mai multe instrumente AI pentru a accelera scrierea codului, pentru debugging și pentru luarea deciziilor de arhitectură. Acest document prezintă concret cum au fost utilizate aceste instrumente.

---

## Instrumente AI Folosite

| Instrument | Scop principal |
|---|---|
| GitHub Copilot | Autocompletare cod, sugestii de funcții |
| ChatGPT (GPT-4) | Debugging, explicații arhitectură, generare documentație |
| Claude (Anthropic) | Revizuire cod, sugestii de refactorizare |

---

## Exemple Concrete de Utilizare

### 1. Generarea structurii agenților AI

**Context:** Trebuia să implementăm doi agenți AI pentru detectarea anomaliilor și predicția stocului.

**Prompt folosit:**
> "Scrie un agent Python care folosește sklearn pentru a detecta tranzacții suspecte dintr-un sistem POS, folosind IsolationForest. Agentul trebuie să se antreneze dinamic pe date reale dacă există suficiente, sau pe date de fallback dacă nu."

**Rezultat:** ChatGPT a generat scheletul funcției `verifica_anomalie_comanda()` din `agent_anomalii.py`. Am adaptat manual:
- Parametrul `contamination=0.1` ajustat după testare
- Adăugat logica de fallback cu date predefinite
- Integrat cu baza de date Oracle prin Django ORM

**Concluzie:** AI a redus timpul de implementare de la ~4 ore estimat la ~1 oră, dar a necesitat validare și adaptare manuală.

---

### 2. Rezolvarea erorilor de conexiune Oracle + Docker

**Context:** La configurarea Docker-ului pentru Oracle SQL, apărea eroarea `DPI-1047: Cannot locate a 64-bit Oracle Client library`.

**Prompt folosit:**
> "Am eroarea DPI-1047 când încerc să conectez Python oracledb cu Oracle în Docker pe Windows. Cum rezolv?"

**Rezultat:** GitHub Copilot a sugerat configurarea `oracledb.init_oracle_client()` și GitHub Copilot Chat a identificat că lipsea variabila de mediu `LD_LIBRARY_PATH` în `Dockerfile`. Am actualizat `Dockerfile`-ul cu setările corecte.

**Concluzie:** Fără AI, debugging-ul ar fi durat câteva ore. Cu AI a durat ~20 minute.

---

### 3. Generarea interogărilor SQL complexe

**Context:** Funcțiile din `FUNCTII_SQL.py` necesitau interogări pentru calculul profitului pe perioade diferite (zilnic/săptămânal/lunar).

**Prompt folosit:**
> "Scrie o funcție Django ORM care calculează profitul net pe o perioadă dată, considerând prețul de vânzare și costul de achiziție al produselor dintr-un model Tranzactie."

**Rezultat:** Copilot a generat baza funcției. Am adaptat pentru structura specifică a modelelor noastre (Oracle SQL cu `oracledb`).

---

### 4. Generarea interfeței grafice cu Flet

**Context:** Niciun membru al echipei nu mai lucrase cu framework-ul Flet anterior.

**Prompt folosit:**
> "Cum creez un tabel interactiv în Flet Python cu butoane de filtrare după dată?"

**Rezultat:** ChatGPT a oferit exemple de cod pentru `ft.DataTable` și `ft.DatePicker`. Am adaptat exemplele pentru modulele `UI_ISTORIC.py` și `UI_RAPOARTE.py`.

---

## Limitele Instrumentelor AI

- **Erori de context:** AI nu cunoștea structura exactă a bazei noastre de date Oracle și genera cod incompatibil cu modelele Django.
- **Cod outdated:** Unele sugestii Copilot foloseau API-uri deprecate din versiuni vechi de `oracledb`.
- **Fără testare:** Codul generat de AI nu a fost niciodată acceptat fără testare manuală.

---

## Concluzii

Instrumentele AI au contribuit semnificativ la accelerarea dezvoltării, în special pentru:
- Reducerea timpului de debugging cu ~60%
- Generarea rapidă a structurii inițiale a fișierelor
- Explicarea conceptelor noi (Flet, oracledb, IsolationForest)

Toate contribuțiile AI au fost revizuite, testate și adaptate manual de membrii echipei. AI a funcționat ca un **asistent de programare**, nu ca un înlocuitor al gândirii critice.
