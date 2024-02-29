from flask import Flask, render_template
import sqlite3

app = Flask(__name__, template_folder='/app')

# Configuration de la base de données SQLite3
DATABASE = '/root/db/botaDB.db'

def connect_db():
    return sqlite3.connect(DATABASE)

# Route pour afficher les données depuis la base de données
@app.route('/')
def afficher_donnees():
    try:
        # Connexion à la base de données
        conn = connect_db()
        cursor = conn.cursor()

        # Exécution d'une requête SELECT (exemple)
        cursor.execute('SELECT * FROM UserDATA;')
        donnees = cursor.fetchall()

        # Fermeture de la connexion à la base de données
        conn.close()

        return render_template('index.html', donnees=donnees)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')
