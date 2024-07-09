from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import sqlite3
import hashlib
import datetime
import jwt
import bdd
import geoVerif

app = Flask(__name__)

@app.route('/inscription', methods=['POST'])
def inscription():
    if request.is_json:
        json_data = request.json
        dico_inscription = {
            'firstname': json_data.get('firstName'),
            'lastname': json_data.get('lastName'),
            'email': json_data.get('email'),
            'password': json_data.get('password'),
            'phone': json_data.get('phone'),
            'userAddress': json_data.get('userAddress'),
            'role_id': json_data.get('roleId'),
            'city_id': json_data.get('cityId'),
            'age': json_data.get('age')
        }
        inscriptionDB = bdd.DataBase()
        valueDB = inscriptionDB.register_to_db(dico_inscription)
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
    if request.is_json:
        json_data = request.json
        dico_login = {
            'email': json_data.get('email'),
            'password': json_data.get('password')
        }
        loginDB = bdd.DataBase()
        valueDB = loginDB.connexion_db(dico_login)
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
    adresses = [(37.4217636, -122.084614), (38.897699700000004, -77.03655315), (51.5008349, -0.1430045264505431), (48.8707573, 2.3053312), (55.7516212, 37.618122044334896)]
    return jsonify(adresses), 200

@app.route('/profile', methods=['POST'])
def profile():
    if request.is_json:
        data = request.json
        token = data.get('token')
        get_profile = bdd.DataBase()
        profile_data = get_profile.profile(token)
        return jsonify(profile_data), 200
    else:
        response = {
            "status": 'No_token send',
            "message": "inscription failed",
        }
        return jsonify(response), 400

@app.route('/addplant', methods=['POST'])
def addPlant():
    if request.is_json:
        data = request.json
        token = data.get('token')
        json_data = request.json
        dico_ajout = {
            'plantDescription': json_data.get('plantDescription'),
            'plantAdress': json_data.get('plantAdress'),
            'name': json_data.get('name'),
            'duree_garde': json_data.get('duree_garde')
        }
        add_plant = bdd.DataBase()
        plant_added = add_plant.Ajout_plante(token, dico_ajout)
        return jsonify("test"), 200
    else:
        response = {
            "status": 'null elies',
            "message": "inscription failed",
        }
        return jsonify(response), 400

@app.route('/send_message', methods=['POST'])
def send_message():
    if request.is_json:
        data = request.json
        sender_id = data.get('sender_id')
        receiver_id = data.get('receiver_id')
        message_text = data.get('message_text')
        
        db = bdd.DataBase()
        db.send_message(sender_id, receiver_id, message_text)
        
        return jsonify({"message": "Message sent successfully"}), 200
    else:
        return jsonify({"error": "Request content is not in JSON format"}), 400

@app.route('/get_messages', methods=['GET'])
def get_messages():
    user_id = request.args.get('user_id')
    
    if user_id:
        db = bdd.DataBase()
        messages = db.get_messages(user_id)
        
        return jsonify(messages), 200
    else:
        return jsonify({"error": "User ID not provided"}), 400

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
