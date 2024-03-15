from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import sqlite3
import hashlib
import datetime
import jwt
#from dotenv import load_dotenv
#import os

#load_dotenv()

#cle_secrete=os.getenv("HASHPASS")
#import requests



def generer_jwt(payload):
    #à enlever
    cle_secrete = '689kjLK^%E4mM#'
    # Ajoute la date d'expiration à la charge utile
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(hours=3)
    
    # Génère le jeton JWT
    jeton = jwt.encode(payload, cle_secrete, algorithm='HS256')
    
    return jeton



def md5_hash(texte):
    # Convertit la chaîne de caractères en bytes (nécessaire pour l'utilisation de hashlib)
    texte_bytes = texte.encode('utf-8')
    # Calcule le hachage MD5
    hachage_md5 = hashlib.md5(texte_bytes)
    # Renvoie la représentation hexadécimale du hachage
    return hachage_md5.hexdigest()

def time_token():
    temps_debut = datetime.datetime.now()
    delta = delta = datetime.timedelta(hours=3)
    temps_fin = temps_debut + delta
    return {"debut":temps_debut , "fin":temps_fin}

DATABASE = '/root/db/botaDB.db'

def connect_db():
    return sqlite3.connect(DATABASE)

class DataBase:
    def __init__(self):
        self.conn = connect_db()
    
    def to_connexionPage(self):
        """
        RENVOYER PAGE DE CONNEXION
        """
        pass


    def connexion_db(self,dico):
        self.conn = connect_db()
        self.dico = dico
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT UserId FROM UserData WHERE email=? and password=?", (self.dico["email"], md5_hash(self.dico["password"])))
        self.connect = self.cursor.fetchone() 
        if self.connect:
            self.cursor = self.conn.cursor()
            time = time_token()
            payload = {'user_id': self.connect,'username': self.dico["email"]}
            self.tokenGen = generer_jwt(payload)
            self.cursor.execute("INSERT INTO Connection (Token,userId, Starting_time, Ending_time) VALUES (?,?,?,?)", (str(self.tokenGen),str(self.connect),time["debut"],time["fin"]))
            self.conn.commit()
            return self.tokenGen
            
        else:
            return 400
        

    def register_to_db(self, dico):
        self.conn = connect_db()
        self.dico = dico
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT email, phone FROM UserData WHERE email=? OR phone=?", (self.dico["email"], self.dico["phone"]))
        self.exist = self.cursor.fetchone()
        if self.exist:
            return self.exist
        else :
            self.cursor = self.conn.cursor()
            #self.cursor.execute("INSERT INTO UserData (firstname,lastname, email, password, phone, userAddress, role_id,cityId, age) VALUES (?,?,?, ?, ?, ?, ?, ?)",(self.dico["firstname"],self.dico["lastname"], self.dico["email"], md5_hash(self.dico["password"]),self.dico["phone"], self.dico["userAddress"], self.dico["role_id"],self.dico["city_id"],str(self.dico["age"])))

            self.cursor.execute("INSERT INTO UserData (firstname,lastname, email, password, phone, userAddress, status,cityId, age) VALUES (?,?,?,?,?, ?,?,?,?)",(self.dico["firstname"],self.dico["lastname"], self.dico["email"], md5_hash(self.dico["password"]),self.dico["phone"], self.dico["userAddress"],self.dico["role_id"],self.dico["city_id"],str(self.dico["age"])))
            self.conn.commit()
            self.insert = self.cursor.fetchone()
            return self.insert
    
    def verification_token(self, token):
        self.conn = connect_db()
        self.cursor = self.conn.cursor()
        self.cursor.execute("SELECT Ending_time, UserId FROM Connection WHERE Token=?", (token,))
        self.timeToken = self.cursor.fetchone()
        self.user_id=self.timeToken[1][1]
        app.logger.info(f'---------------------------------------------------\n\n\nvoici le user :{self.user_id}, \t {self.timeToken[0]}\n\n\n---------------------------- ')
        self.time_tokenStr = datetime.datetime.strptime(self.timeToken[0], "%Y-%m-%d %H:%M:%S.%f")
        if self.timeToken and self.time_tokenStr > datetime.datetime.now():
            return self.user_id
        else:
            return False 
    

    
    def profile(self, token):
        self.is_connect = self.verification_token(token)
        if self.is_connect:
            self.conn = connect_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT email, firstname,lastname,userAddress,cityId,age FROM UserData WHERE UserId =?", (self.is_connect))
            self.rows = self.cursor.fetchall()
            self.resultat = {
                "email": self.rows[0],
                "firstname": self.rows[1],
                "lastname": self.rows[2],
                "userAddress": self.rows[3],
                "cityId": self.rows[4],
                "age": self.rows[5]
                }
            return self.resultat
        else:
            self.to_connexionPage()

    def coordonnee_gps(self, adresse):
        pass

#Peut être trouver le coordonnée

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

        inscriptionDB = DataBase()
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

        loginDB = DataBase()
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
        app.logger.info(f'---------------------------------------------------\n\n\nvoici le token :{token}\n\n\n---------------------------- ')
        get_profile= DataBase()
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

