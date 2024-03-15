from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import sqlite3
import hashlib
import datetime
import jwt
import bdd


app = Flask(__name__)
    
    # def informations_plante(self, id_plante):
    #     # Exécuter la requête pour récupérer les informations de la plante par son ID
    #     self.cursor.execute("SELECT nom, emplacement, description, frequence_arrosage, exposition_lumiere, engrais, problemes_courants, conseils_speciaux FROM Plant WHERE id=?", (id_plante,))
    #     plante_data = self.cursor.fetchone()

    #     # Vérifier si des données ont été trouvées pour l'ID de la plante donné
    #     if plante_data:
    #         # Créer un dictionnaire avec les informations de la plante
    #         plante_info = {
    #             "nom": plante_data[0],
    #             "emplacement": plante_data[1],
    #             "description": plante_data[2],
    #             "frequence_arrosage": plante_data[3],
    #             "exposition_lumiere": plante_data[4],
    #             "engrais": plante_data[5],
    #             "problemes_courants": plante_data[6],
    #             "conseils_speciaux": plante_data[7]
    #         }
    #         return plante_info
    #     else:
    #         # Retourner None si aucune donnée n'est trouvée pour l'ID de la plante donné
    #         return None

@app.route('/inscription', methods=['POST'])
def inscription():
    # Vérifie si le contenu de la requête est en format JSON
    if request.is_json:
        # Récupère le JSON à partir du corps de la requête
        json_data = request.json
        
        # Traitement du JSON
        dico_inscription = {
        'firstname': json_data.get('firstName'),
        'lastname': json_data.get('lastName'),
        'email': json_data.get('email'),
        'password': json_data.get('password'),
        'phone': json_data.get('phone'),
        'userAddress': json_data.get('userAddress'),
        'role_id': json_data.get('roleId'),
        'city_id': json_data.get('cityId'),
        'age':json_data.get('age')
        }

        inscriptionDB = bdd.DataBase()
        valueDB =inscriptionDB.register_to_db(dico_inscription)
        if valueDB == 200:
            response = {
                "status": str(valueDB),
                "message": "Inscrit",
            }
            return jsonify(response), 400
        else:
            response = {
                "status": str(valueDB),
                "message": "inscription OK",
            }
            return jsonify(response), 200

        
    else:
        return jsonify({"error": "Contenu de la requête n'est pas en format JSON"}), 400
    
@app.route('/login', methods=['POST'])
def login():
    # Vérifie si le contenu de la requête est en format JSON
    if request.is_json:
        # Récupère le JSON à partir du corps de la requête
        json_data = request.json
        
        # Traitement du JSON
        dico_login = {
        'email': json_data.get('email'),
        'password': json_data.get('password')
        }

        loginDB = bdd.DataBase()
        valueDB =loginDB.connexion_db(dico_login)
        if valueDB != 400:
            response = {
                "token": str(valueDB),
                "message": "Inscrit",
            }
            return jsonify(response), 200
        else:
            response = {
                "status": str(valueDB),
                "message": "inscription failed",
            }
            return jsonify(response), 400

        
    else:
        return jsonify({"error": "Contenu de la requête n'est pas en format JSON"}), 400



@app.route('/recupererlocalisation', methods=['GET'])
def recupererlocalisation():
    # Supposons que les coordonnées GPS sont déjà définies
    adresses = [(37.4217636, -122.084614), (38.897699700000004, -77.03655315), (51.5008349, -0.1430045264505431), (48.8707573, 2.3053312), (55.7516212, 37.618122044334896)]
    # Retourner les coordonnées GPS sous forme de liste
    return jsonify(adresses), 200

@app.route('/profile', methods=['POST'])
def profile():
    if request.is_json:
        data = request.json
        token = data.get('token')
        get_profile= bdd.DataBase()
        profile_data = get_profile.profile(token)
        return jsonify(profile_data), 200
    
    else:
        response = {
            "status": 'null elies',
            "message": "inscription failed",
        }
        return jsonify(response), 400
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

