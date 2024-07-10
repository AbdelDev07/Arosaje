import sqlite3
import mysql.connector

# Connexion à la base SQLite
sqlite_conn = sqlite3.connect('/root/db/botaDB.db')
sqlite_cursor = sqlite_conn.cursor()

# Connexion à la base MySQL
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='Arosaje',
    password='Arosaje',
    database='AjosajeDB'
)
mysql_cursor = mysql_conn.cursor()

# Transfert des données
sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = sqlite_cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    for row in rows:
        placeholders = ', '.join(['%s'] * len(row))
        mysql_cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)
    
    mysql_conn.commit()

# Fermer les connexions
sqlite_conn.close()
mysql_conn.close()
