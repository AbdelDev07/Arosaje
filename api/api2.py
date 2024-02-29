# Importez les classes nécessaires de Flask
from flask import Flask, render_template
import sqlite3

# Créez une instance de l'application Flask
app = Flask(__name__)

# Chemin de la base de données
DATABASE = "/root/db/boteDB.db"

# Fonction pour établir une connexion à la base de données
def connect_db():
    return sqlite3.connect(DATABASE)

# Route principale pour afficher les données de la base de données
@app.route('/')
def index():
    # Récupérer les données de la base de données
    data = get_data_from_database()
    
    # Renvoyer les données à un modèle HTML
    return render_template('index.html', data=data)

# Fonction pour récupérer les données de la base de données
def get_data_from_database():
    conn = connect_db()
    cursor = conn.cursor()

    # Exécutez votre requête SQL pour récupérer les données nécessaires
    # Exemple: cursor.execute("SELECT * FROM UserData")
    # data = cursor.fetchall()

    # Exemple: Si vous avez la table UserData, vous pouvez récupérer les noms
    cursor.execute("SELECT firstName, lastName FROM UserData")
    data = cursor.fetchall()

    # Assurez-vous de fermer la connexion après avoir récupéré les données
    conn.close()

    # Retournez les données récupérées
    return data

# Exécutez l'application Flask
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
