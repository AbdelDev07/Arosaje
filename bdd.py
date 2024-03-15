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


#Peut être trouver le coordonnée


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
            self.cursor.execute("SELECT email, firstname,lastname,userAddress,cityId FROM UserData WHERE UserId =?", (self.is_connect))
            self.rows = self.cursor.fetchall()
            self.rows= self.rows[0]

            self.resultat = {
                "email": self.rows[0],
                "nom": self.rows[1],
                "lastname": self.rows[2],
                "adresse": self.rows[3],
                "ville": self.rows[4]
                }
            return self.resultat
        else:
            self.to_connexionPage()

    def Ajout_plante(self, token):
        self.is_connect = self.verification_token(token)
        if self.is_connect:
            self.conn = connect_db()
            self.cursor = self.conn.cursor()
            self.cursor.execute("INSERT INTO UserData (firstname,lastname, email, password, phone, userAddress, status,cityId, age) VALUES (?,?,?,?,?, ?,?,?,?)",(self.dico["firstname"],self.dico["lastname"], self.dico["email"], md5_hash(self.dico["password"]),self.dico["phone"], self.dico["userAddress"],self.dico["role_id"],self.dico["city_id"],str(self.dico["age"])))
            self.conn.commit()
            self.insert = self.cursor.fetchone()

            self.resultat = {
                "email": self.rows[0],
                "nom": self.rows[1],
                "lastname": self.rows[2],
                "adresse": self.rows[3],
                "ville": self.rows[4]
                }
            return self.resultat
        else:
            self.to_connexionPage()

    def coordonnee_gps(self, adresse):
        pass
