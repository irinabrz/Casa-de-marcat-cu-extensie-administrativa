import numpy as np
from sklearn.ensemble import IsolationForest

def verifica_anomalie_comanda(cantitate_curenta, valoare_curenta, tip_plata_id, istoric_comenzi_db=None):
    """
    Antrenează local un model Isolation Forest și verifică dacă tranzacția curentă este suspectă.
    """
    if istoric_comenzi_db and len(istoric_comenzi_db) >= 5:
        date_antrenament = np.array(istoric_comenzi_db)
        print(f"[ AI INFO] Re-antrenare dinamică utilizând {len(date_antrenament)} tranzacții reale din Oracle.")
    else:
        date_antrenament = np.array([
            [1, 12.0, 1],  [1, 15.0, 1],  [2, 24.0, 1],  [2, 30.0, 1],
            [1, 18.0, 1],  [3, 45.0, 1],  [2, 28.0, 1],  [4, 60.0, 1],
            [1, 14.0, 1],  [2, 35.0, 1],  [1, 15.0, 1],  [3, 42.0, 1]
        ])
        print("[ AI INFO] Date insuficiente în Oracle. Se utilizează setul de antrenament predefinit.")
    
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(date_antrenament)
    comanda_curenta = np.array([[cantitate_curenta, valoare_curenta, tip_plata_id]])
    predictie = model.predict(comanda_curenta)
    
    if predictie[0] == -1:
        return True
    return False