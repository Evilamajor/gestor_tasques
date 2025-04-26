import psycopg2

def get_db_connection():
    conn = psycopg2.connect(
        dbname='gestor_tasques',
        user='postgres',
        password='novaContrasenyaSegura',  # Substitueix per la teva
        host='localhost'
    )
    return conn
