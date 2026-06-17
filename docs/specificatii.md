# Specificații Proiect — Casa de Marcat cu Extensie Administrativă

**Disciplina:** Metode de Dezvoltare Software (MDS)  
**Echipă:** irinabrz + colaboratori  
**Tehnologii:** Python 3.14, Django 6.0, Flet, Oracle SQL, Docker, scikit-learn

---

## 1. Descrierea Proiectului

Aplicația este un sistem modern de gestiune pentru o cafenea, care combină funcționalitățile unui **POS (Point of Sale)** clasic cu o **extensie administrativă** bazată pe inteligență artificială. Sistemul permite procesarea vânzărilor, gestionarea stocurilor, generarea de rapoarte financiare și detectarea automată a anomaliilor și riscurilor de stoc.

---

## 2. Cerințe Funcționale

### CF1 — Modul Vânzări (POS)
- **CF1.1** Operatorul poate adăuga produse într-un coș de cumpărături
- **CF1.2** Sistemul acceptă plata prin cash sau card
- **CF1.3** La finalizarea vânzării, stocul produselor se actualizează automat
- **CF1.4** Agentul AI verifică automat dacă tranzacția este suspectă (anomalie)
- **CF1.5** Sistemul afișează totalul de plată în timp real

### CF2 — Modul Stocuri
- **CF2.1** Administratorul poate vizualiza stocul curent al tuturor produselor
- **CF2.2** Sistemul alertează automat când un produs are stoc scăzut
- **CF2.3** Agentul AI predictiv estimează în câte zile se va epuiza stocul unui produs
- **CF2.4** Administratorul poate adăuga stoc nou pentru orice produs

### CF3 — Modul Rapoarte
- **CF3.1** Sistemul generează grafice de venituri vs. costuri (zilnic/săptămânal/lunar)
- **CF3.2** Administratorul poate exporta rapoarte în format PDF
- **CF3.3** Sistemul calculează profitul net pe orice perioadă selectată

### CF4 — Modul Istoric
- **CF4.1** Utilizatorul poate vizualiza toate tranzacțiile anterioare
- **CF4.2** Istoricul poate fi filtrat după dată

### CF5 — Modul Marfă
- **CF5.1** Administratorul poate adăuga produse noi în sistem
- **CF5.2** Administratorul poate modifica prețul și costul de achiziție al produselor

---

## 3. Cerințe Non-Funcționale

| ID | Cerință | Criteriu de acceptare |
|---|---|---|
| CNF1 | Portabilitate | Rulează identic pe Windows, Mac, Linux prin Docker |
| CNF2 | Performanță | Înregistrarea unei vânzări durează < 2 secunde |
| CNF3 | Disponibilitate | Baza de date Oracle rulează persistent în container Docker |
| CNF4 | Securitate | Credențialele DB nu sunt hardcodate în cod sursă public |
| CNF5 | Scalabilitate | Sistemul suportă minim 1000 de produse și 10.000 de tranzacții |

---

## 4. Backlog Proiect

### ✅ Funcționalități Implementate (Done)
- [x] Înregistrarea comenzilor cu plată cash/card
- [x] Actualizarea automată a stocului la vânzare
- [x] Vizualizarea profitului zilnic/săptămânal/lunar
- [x] Istoric comenzi cu filtrare după dată
- [x] Alertă automată pentru stoc scăzut
- [x] Grafice venituri vs. pierderi (Matplotlib)
- [x] Export rapoarte PDF (FPDF2)
- [x] Agent AI anomalii (IsolationForest)
- [x] Agent AI predictiv stoc (LinearRegression)
- [x] Containerizare Docker (Oracle + aplicație)
- [x] Teste automate conexiune DB și funcționalitate vânzare

### 🔄 Funcționalități în Lucru / Viitoare
- [ ] Sistem de autentificare (login cu rol operator/administrator)
- [ ] Notificări push pentru alerte de stoc
- [ ] Dashboard cu statistici în timp real
- [ ] Export date în format Excel (XLSX)
- [ ] Suport multi-cafenea (mai multe locații)

---

## 5. Definiția lui "Done" (Definition of Done)

O funcționalitate este considerată **completă** când:
1. Codul este scris și funcționează local
2. A fost testat manual cu date reale
3. Nu produce erori în consolă
4. A fost pusă pe branch-ul personal și mergeată în `main` prin Pull Request
5. README-ul este actualizat dacă e cazul
