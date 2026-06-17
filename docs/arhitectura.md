# Arhitectura Aplicației

Acest document descrie arhitectura sistemului **Casa de Marcat cu Extensie Administrativă**, incluzând diagrama componentelor, diagrama claselor și workflow-ul principal.

---

## 1. Diagrama Componentelor

```mermaid
graph TB
    subgraph UI["🖥️ Interfață Grafică (Flet)"]
        UV[UI_VANZARE.py]
        US[UI_STOCURI.py]
        UR[UI_RAPOARTE.py]
        UI2[UI_ISTORIC.py]
        UD[UI_DASHBOARD.py]
        UM[UI_MARFA.py]
    end

    subgraph LOGIC["⚙️ Logică Business"]
        SQL[FUNCTII_SQL.py]
    end

    subgraph AI["🤖 Agenți AI (sklearn local)"]
        AA[agent_anomalii.py\nIsolationForest]
        AP[agent_predictiv_stoc.py\nLinearRegression]
    end

    subgraph BACKEND["🔧 Backend Django"]
        CFG[CONFIG_SISTEM/\nSettings + Conexiune]
        MOD[LOGICA_DATABASE/\nModele ORM]
    end

    subgraph DB["🗄️ Bază de Date"]
        ORA[(Oracle SQL\nDocker Container)]
    end

    UV --> SQL
    US --> SQL
    UR --> SQL
    UI2 --> SQL
    UD --> SQL
    UM --> SQL

    UV --> AA
    US --> AP

    SQL --> MOD
    MOD --> CFG
    CFG --> ORA
```

---

## 2. Diagrama Claselor (Modele Django)

```mermaid
classDiagram
    class Produs {
        +int id
        +string nume_produs
        +float pret
        +float cost_achizitie
        +int stoc_curent
        +string categorie
    }

    class Angajat {
        +int id
        +string nume
        +string prenume
        +string rol
        +string email
    }

    class Client {
        +int id
        +string nume
        +string telefon
        +int puncte_fidelitate
    }

    class Tranzactie {
        +int id
        +int cantitate
        +float pret_total
        +string metoda_plata
        +datetime data_creare
    }

    class ItemTranzactie {
        +int id
        +int cantitate
        +float pret_unitar
    }

    Angajat "1" --> "0..*" Tranzactie : procesează
    Client "0..1" --> "0..*" Tranzactie : efectuează
    Tranzactie "1" --> "1..*" ItemTranzactie : conține
    Produs "1" --> "0..*" ItemTranzactie : apare în
```

---

## 3. Workflow: Procesarea unei Vânzări

```mermaid
sequenceDiagram
    actor Operator
    participant UI as UI_VANZARE.py
    participant SQL as FUNCTII_SQL.py
    participant AI as agent_anomalii.py
    participant ORM as Django ORM
    participant DB as Oracle SQL

    Operator->>UI: Adaugă produse în coș
    Operator->>UI: Apasă "Finalizează vânzarea"
    
    UI->>AI: verifica_anomalie_comanda(cantitate, valoare, tip_plata)
    AI-->>UI: True (suspect) / False (normal)
    
    alt Tranzacție suspectă
        UI-->>Operator: Avertizare anomalie detectată
    end

    UI->>SQL: inregistreaza_vanzare(angajat, produse, metoda_plata)
    SQL->>ORM: Creează obiect Tranzactie
    SQL->>ORM: Scade stoc pentru fiecare produs
    ORM->>DB: INSERT INTO tranzactie...
    ORM->>DB: UPDATE produs SET stoc = stoc - cantitate...
    DB-->>ORM: Confirmare
    ORM-->>SQL: Obiect Tranzactie salvat
    SQL-->>UI: Succes
    UI-->>Operator: Bon afișat, stoc actualizat
```

---

## 4. Workflow: Predicție Stoc

```mermaid
sequenceDiagram
    actor Admin
    participant UI as UI_STOCURI.py
    participant AP as agent_predictiv_stoc.py
    participant ORM as Django ORM
    participant DB as Oracle SQL

    Admin->>UI: Deschide modulul Stocuri
    UI->>AP: estimeaza_zile_ramase_stoc_ai(id_produs)
    AP->>ORM: Produs.objects.get(id)
    ORM->>DB: SELECT * FROM produs WHERE id=...
    DB-->>ORM: Date produs (stoc, nume)
    AP->>ORM: Tranzactie.objects.filter(produs_id)
    ORM->>DB: SELECT * FROM tranzactie WHERE produs_id=...
    DB-->>ORM: Istoric vânzări
    
    AP->>AP: Antrenează LinearRegression pe istoric
    AP->>AP: Calculează rata de vânzare/zi
    AP->>AP: Estimează zile până la epuizare
    
    AP-->>UI: (alert, zile_ramase, nume_produs)
    
    alt Stoc critic (< 3 zile)
        UI-->>Admin: ⚠️ Alertă: [produs] se epuizează în X zile!
    else Stoc OK
        UI-->>Admin: ✅ Stoc suficient
    end
```

---

## 5. Arhitectura de Deployment (Docker)

```mermaid
graph LR
    subgraph HOST["💻 Calculator Local"]
        subgraph DOCKER["🐳 Docker Desktop"]
            ORA[(Oracle DB\nFreePDB1\nPort: 1521)]
        end
        
        APP["🐍 Aplicație Python\nFlet + Django\nRulează local\n(nu în Docker)"]
    end

    APP -->|"oracledb\nlocalhost:1521"| ORA
    USER["👤 Utilizator"] -->|"Interfață grafică\nFlet"| APP
```

> **Notă:** Aplicația Python rulează direct pe sistemul de operare (nu în container), dar se conectează la baza de date Oracle care rulează în Docker. Aceasta permite o interfață grafică nativă prin Flet.
