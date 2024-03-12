from flask import Flask, request, jsonify, render_template, redirect, url_for, abort
import sqlite3
import hashlib
import datetime
import jwt
#import requests



def generer_jwt(payload):
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
    
    def to_connexionPage():
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
        self.cursor.execute("SELECT Ending_time, User_id FROM Connection WHERE Token=?", (token))
        self.timeToken = self.cursor.fetchone()
        if self.timeToken and self.timeToken[0] < datetime.datetime.now():
            return self.timeToken[1]
        else:
            return False 
    

    
    def profile(self, token):
        self.is_connect = self.verification_token(token)
        if self.is_connect:
            self.conn = connect_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT email, firstname,lastname,userAddress,cityId,age FROM UserData WHERE User_id =?", (self.is_connect))
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
    adresses = [
    "1600 Amphitheatre Parkway, Mountain View, CA 94043, États-Unis",  # Googleplex
    "One Apple Park Way, Cupertino, CA 95014, États-Unis",  # Apple Park
    "1600 Pennsylvania Ave NW, Washington, DC 20500, États-Unis",  # Maison Blanche
    "Buckingham Palace, Westminster, London SW1A 1AA, Royaume-Uni",  # Buckingham Palace
    "Champs-Élysées, 75008 Paris, France",  # Avenue des Champs-Élysées
    "Kremlin, Moscou, Russie"
    ]
    
    # Retourner les coordonnées GPS sous forme de liste
    return jsonify(adresses), 200

@app.route('/profile', methods=['GET'])
def profile():
    token = request.args.get('token')
    get_profile= DataBase()
    profile_data = get_profile.profile(token)
    
    # Retourner les coordonnées GPS sous forme de liste
    return jsonify(profile_data), 200
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")

