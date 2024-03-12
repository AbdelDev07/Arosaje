import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:mspr/accueil_page.dart';
import 'package:mspr/inscription_page.dart';

class LoginPage extends StatelessWidget {
  LoginPage({Key? key});

  // URL de l'API de connexion
  static const String url = 'https://api.arosaje.a-hamidi.fr/login';

  final storage = FlutterSecureStorage();

  // Fonction pour récupérer le token du stockage sécurisé
  Future<String?> getToken() async {
    return await storage.read(key: 'token');
  }

  // Fonction pour enregistrer le token dans le stockage sécurisé
  Future<void> saveToken(String token) async {
    await storage.write(key: 'token', value: token);
  }

  // Fonction de connexion
  Future<void> login(
      BuildContext context, String email, String password) async {
    try {
      final response = await http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'email': email, 'password': password}),
      );

      if (response.statusCode == 200) {
        final responseData = jsonDecode(response.body);
        final token = responseData['token'];

        // Enregistrement du token
        await saveToken(token);

        // Navigation vers la page d'accueil après connexion réussie
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const AccueilPage()),
        );
      } else if (response.statusCode == 401) {
        // En cas d'erreur d'authentification
        ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
          content: Text('Email ou mot de passe incorrect.'),
        ));
      } else {
        // En cas d'erreur autre que l'erreur d'authentification
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(
          content:
              Text('Une erreur s\'est produite. Veuillez réessayer plus tard.'),
        ));
      }
    } catch (error) {
      // En cas d'erreur lors de la connexion
      print('Erreur lors de la connexion : $error');

      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content:
            Text('Une erreur s\'est produite. Veuillez réessayer plus tard.'),
      ));
    }
  }

  @override
  Widget build(BuildContext context) {
    TextEditingController emailController = TextEditingController();
    TextEditingController passwordController = TextEditingController();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Connexion'),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                // Logo
                GestureDetector(
                  onTap: () {
                    // Naviguer vers la page d'accueil en cliquant sur le logo
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => const AccueilPage()),
                    );
                  },
                  child: Image.network(
                    'https://media.discordapp.net/attachments/1194280434889146411/1195383436957986967/logo_site-removebg-preview_1.png?ex=65fd9e94&is=65eb2994&hm=b6bac77d183cb9826660ef726867f7e33893adcec9d58826dbf8653fa86a897c&=&format=webp&quality=lossless&width=1000&height=500',
                    width: 300,
                    height: 300,
                  ),
                ),
                const SizedBox(height: 30),
                // Champ d'email
                TextField(
                  controller: emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),
                // Champ de mot de passe
                TextField(
                  controller: passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Mot de passe',
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 20),
                // Bouton de connexion
                ElevatedButton(
                  onPressed: () {
                    login(
                        context, emailController.text, passwordController.text);
                  },
                  child: const Text('Connexion'),
                ),
                const SizedBox(height: 10),
                // Bouton pour naviguer vers la page d'inscription
                TextButton(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => InscriptionPage()),
                    );
                  },
                  child: const Text('Pas encore inscrit ? Inscrivez-vous'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
