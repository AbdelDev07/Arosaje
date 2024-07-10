import sqlite3
import mysql.connector

def get_sqlite_table_structure(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return cursor.fetchall()

def create_mysql_table_from_sqlite(mysql_cursor, table_name, columns):
    col_defs = []
    for col in columns:
        col_name, col_type, not_null, default_val, pk = col[1], col[2], col[3], col[4], col[5]
        # Convert SQLite type to MySQL type
        mysql_col_type = "INT" if col_type.startswith("INT") else col_type
        col_def = f"`{col_name}` {mysql_col_type}"
        if pk:
            col_def += " PRIMARY KEY"
        if mysql_col_type == "INT" and pk and "AUTO_INCREMENT" in col_type:
            col_def += " AUTO_INCREMENT"
        if not_null:
            col_def += " NOT NULL"
        if default_val is not None:
            col_def += f" DEFAULT '{default_val}'"
        col_defs.append(col_def)
    
    col_defs_str = ", ".join(col_defs)
    create_table_query = f"CREATE TABLE IF NOT EXISTS `{table_name}` ({col_defs_str});"
    mysql_cursor.execute(create_table_query)

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
    
    # Recréer la table dans MySQL
    columns = get_sqlite_table_structure(sqlite_cursor, table_name)
    create_mysql_table_from_sqlite(mysql_cursor, table_name, columns)
    
    # Transférer les données
    sqlite_cursor.execute(f"SELECT * FROM {table_name}")
    rows = sqlite_cursor.fetchall()
    
    for row in rows:
        placeholders = ', '.join(['%s'] * len(row))
        mysql_cursor.execute(f"INSERT INTO {table_name} VALUES ({placeholders})", row)
    
    mysql_conn.commit()

# Fermer les connexions
sqlite_conn.close()
mysql_conn.close()
