from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import UserData

# Créez une instance SQLAlchemy (mais n'initialisez pas encore avec l'application)
db = SQLAlchemy()

def create_app():
    # Créez l'application Flask
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////root/db/botaDB.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialisez l'application Flask avec l'instance SQLAlchemy
    db.init_app(app)

    return app

# Obtenez l'application Flask avec l'instance SQLAlchemy
app = create_app()

# Importez vos modèles après la création de l'application et de l'instance db
from models import UserData

# Exemple de route pour récupérer toutes les données de UserData
@app.route('/all_user_data', methods=['GET'])
def get_all_user_data():
    # Assurez-vous d'exécuter votre code à l'intérieur du contexte de l'application
    with app.app_context():
        # Récupérer toutes les données de la table UserData
        all_user_data = UserData.query.all()

        # Créez une liste pour stocker les données
        user_data_list = []
        for user_data in all_user_data:
            user_data_dict = {
                'userId': user_data.userId,
                'firstName': user_data.firstName,
                'lastName': user_data.lastName,
                'age': user_data.age,
                'email': user_data.email
            }
            user_data_list.append(user_data_dict)

        # Retournez les données en format JSON
        return jsonify({'user_data': user_data_list})

if __name__ == '__main__':
    # Exécutez l'application Flask en mode debug
    app.run(host='0.0.0.0',debug=True)

