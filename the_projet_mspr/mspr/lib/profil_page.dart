import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class ProfilPage extends StatefulWidget {
  final String token;

  const ProfilPage({Key? key, required this.token}) : super(key: key);

  @override
  _ProfilPageState createState() => _ProfilPageState();
}

class _ProfilPageState extends State<ProfilPage> {
  String _prenom = 'Elies';
  String _nom = 'gazoni';
  String _email = 'elies-gazoni@live.fr';
  String _ville = 'Londres';
  String _adresse = '2 rues montant au chateaux';

  @override
  void initState() {
    super.initState();
    // Appel à la fonction pour récupérer les informations de l'utilisateur dès que la page est construite
    fetchData();
  }

  // Fonction pour récupérer les informations de l'utilisateur depuis le backend
  Future<void> fetchData() async {
    try {
      final response = await http.post(
        Uri.parse('http://api.arosaje.a-hamidi.fr/profile'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${widget.token}'
        },
      );

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        setState(() {
          _prenom = data['prenom'];
          _nom = data['nom'];
          _email = data['email'];
          _ville = data['ville'];
          _adresse = data['adresse'];
        });
      } else {
        print('Erreur: ${response.statusCode}');
      }
    } catch (e) {
      print('Erreur: $e');
    }
  }

  void logout() {
    Navigator.popUntil(context, ModalRoute.withName('/'));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil'),
        actions: [
          IconButton(
            icon: Icon(Icons.exit_to_app),
            onPressed: logout,
          ),
        ],
      ),
      body: Container(
        decoration: const BoxDecoration(
          gradient: LinearGradient(
            begin: Alignment.topCenter,
            end: Alignment.bottomCenter,
            colors: [Colors.lightGreenAccent, Colors.green],
          ),
        ),
        child: Center(
          child: SingleChildScrollView(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                const SizedBox(
                  height: 120,
                  width: 120,
                  child: CircleAvatar(
                    backgroundColor: Colors.blue,
                    radius: 60,
                    child: Icon(
                      Icons.person,
                      size: 80,
                      color: Colors.white,
                    ),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  '$_prenom $_nom',
                  style: const TextStyle(
                      fontSize: 20, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 8),
                Text(
                  _email,
                  style: const TextStyle(fontSize: 16),
                ),
                const SizedBox(height: 8),
                Text(
                  'Ville: $_ville',
                  style: const TextStyle(fontSize: 16),
                ),
                const SizedBox(height: 8),
                Text(
                  'Adresse: $_adresse',
                  style: const TextStyle(fontSize: 16),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
