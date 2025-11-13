from flask import Flask
import os
import pyodbc

app = Flask(__name__)

def get_db_connection():
    # Odczytaj connection string
    conn_str = os.environ.get('SQLAZURECONNSTR_DB_CONNECTION_STRING')
    
    # --- WAŻNY KROK DEBUGOWANIA ---
    # Sprawdź, czy connection string został w ogóle odczytany
    if not conn_str:
        # Jeśli go nie ma, zwróć błąd, który to jasno powie
        raise ValueError("Zmienna środowiskowa SQLAZURECONNSTR_DB_CONNECTION_STRING nie została znaleziona!")
    
    # Jeśli istnieje, spróbuj się połączyć
    conn = pyodbc.connect(conn_str)
    return conn

@app.route('/')
def index():
    tasks_html = "<h2>Lista zadan z bazy danych:</h2><ul>"
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT Title FROM Tasks")
        rows = cursor.fetchall()
        for row in rows:
            tasks_html += f"<li>{row.Title}</li>"
        conn.close()
    except Exception as e:
        # Wyświetl dokładny błąd, który wystąpił
        tasks_html += f"<li>Blad polaczenia z baza: {str(e)}</li>"

    tasks_html += "</ul>"
    return tasks_html