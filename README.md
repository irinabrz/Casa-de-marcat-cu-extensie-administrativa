# Casa-de-marcat-cu-extensie-administrativa(MDS Project)

Acesta este un sistem modern de gestiune pentru o cafenea, dezvoltat ca proiect pentru disciplina **Metode Dezvoltare Software (MDS)**. Aplicația integrează o bază de date **Oracle SQL**, o logică prin **Django** și o interfață grafică modernă realizată în **Flet**.

---

## Tehnologii Utilizate

* **Limbaj:** Python 3.14+
* **Framework Logic (Backend):** [Django 6.0](https://www.djangoproject.com/)
* **Interfață Grafică (Frontend):** [Flet (Flutter for Python)](https://flet.dev/)
* **Bază de Date:** Oracle SQL (prin `oracledb`)
* **Rapoarte:** Matplotlib (Grafice) și FPDF2 (Generare PDF)

---

## Structura Proiectului

Proiectul este organizat modular pentru a permite lucrul în echipă pe branch-uri separate:

* `START_APP.py`: Punctul de intrare în aplicație.
* `CONFIG_SISTEM/`: Configurările principale Django și conexiunea la Oracle.
* `LOGICA_DATABASE/`: Definirea modelelor (tabelelor) și migrărilor SQL.
* `UI_VANZARE.py`: Modulul pentru procesarea comenzilor (POS).
* `UI_STOCURI.py`: Gestionarea inventarului și alerte stoc scăzut.
* `UI_RAPOARTE.py`: Statistici vizuale, profit și export PDF.
* `FUNCTII_SQL.py`: Interogări personalizate și calcule financiare.

---

 ## Ghid de Instalare și Rulare (Echipe)

Pentru a asigura un mediu de lucru identic pentru toți membrii echipei, folosim **Docker**. Urmați pașii de mai jos în ordine:

### 1. Prerechizite
1. Descărcați și instalați **[Docker Desktop](https://www.docker.com/products/docker-desktop/)**.
2. **Porniți Docker Desktop** și asigurați-vă că motorul Docker este activ (iconița cu balena este verde).

### 2. Clonarea și Sincronizarea (Git)
Dacă ești prima dată aici, clonează repo-ul. Dacă îl ai deja, **mută-te pe branch-ul tău** și adu ultimele modificări de pe `main`:

```bash
git checkout Branch-NumeleTau #branchurile se pot vedea mai sus, sunt cu numele voastre
git pull origin main
```
3. Pornirea Infrastructurii (Baza de Date + Server)
Deschide terminalul în folderul proiectului și rulează:

```Bash
docker-compose up -d --build
```
Notă: Prima rulare va dura câteva minute (se descarcă imaginea de Oracle).

4. Setup Biblioteci Locale
Deoarece interfața grafică (Flet) rulează direct pe sistemul vostru de operare, trebuie să instalați dependențele și local:

```Bash
pip install -r requirements.txt
```
5. Verificarea Conexiunii
Înainte de a scrie cod, verifică dacă aplicația ta poate comunica cu baza de date Oracle din Docker, folosind fisierul creeat speciat pentru test:

```Bash
python test_db.py
```
Dacă primești mesajul: "SUCCESS: Conexiunea la baza de date a reușit!", ești gata de lucru.

6. Pornirea Aplicației
După ce testul de conexiune a trecut, lansează interfața grafică:

```Bash
python START_APP.py
```

## Funcționalități Implementate (Cerințe Proiect)

- [x]Înregistrarea comenzilor și a plăților (cash, card).
- [x]Vizualizarea totalului câștigat pe zi.
- [x]Vizualizarea profitului zilnic/saptamanal/lunar.
- [x]Istoric comenzi și posibilitatea de filtrare după dată.
- [x]Gestionarea inventarului și a achizițiilor.
- [x]Alertă automată pentru produsele cu stoc scăzut.
- [x]Generarea de statistici vizuale (grafice venituri vs pierderi).
- [x]Exportul rapoartelor în format PDF.