from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process_json', methods=['POST'])
def process_json():
    # Vérifie si le contenu de la requête est en format JSON
    if request.is_json:
        # Récupère le JSON à partir du corps de la requête
        json_data = request.json
        
        # Traitement du JSON
        print("JSON reçu :", json_data)
        
        # Vous pouvez maintenant manipuler les données JSON comme un dictionnaire Python
        # Par exemple, vous pouvez accéder à des clés spécifiques :
        email = json_data.get('email')
        password = json_data.get('password')
        
        # Faire quelque chose avec les données...

        # Renvoie une réponse JSON pour illustrer la manipulation
        response = {
            "status": "success",
            "message": "JSON traité avec succès",
            "email": email,
            "password": password
        }
        
        return jsonify(response), 200
    else:
        return jsonify({"error": "Contenu de la requête n'est pas en format JSON"}), 400

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0")

