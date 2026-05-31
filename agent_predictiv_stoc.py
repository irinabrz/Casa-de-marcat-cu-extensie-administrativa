import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

def estimeaza_zile_ramase_stoc_ai(id_produs_curent):
    """
    Analizează istoricul vânzărilor din Oracle pentru un produs și estimează 
    în câte zile stocul va ajunge la 0 folosind un model local de Regresie Liniară.
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
            return False, 999, produs.nume_produs

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
        print(f"[ AI PREDICT ERROR] Defecțiune la modelul predictiv: {e}")
        return False, 999, ""