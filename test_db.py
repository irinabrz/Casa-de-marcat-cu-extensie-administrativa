import oracledb
import sys

def test_connection():
    print("--- Test Conexiune Oracle SQL în Docker ---")
    try:
        conn = oracledb.connect(
            user="system",
            password="MDS_Cafenea_2026",
            dsn="localhost:1521/FREEPDB1"
        )
        print("SUCCESS: Conexiunea la baza de date a reușit!")
        print(f"Versiune Server Oracle: {conn.version}")
        conn.close()
    except Exception as e:
        print(f" EROARE: Nu s-a putut stabili conexiunea.")
        print(f"Detaliu eroare: {e}")
        print("\nAsigură-te că containerul 'oracle_db' este pornit în Docker Desktop!")

if __name__ == "__main__":
    test_connection()