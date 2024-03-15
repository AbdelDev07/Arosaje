import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:mspr/login_page.dart';

// Classe modèle pour les données utilisateur
class UserData {
  final String firstName;
  final String lastName;
  final int age;
  final String email;
  final String phone;
  final int roleId;
  final String userAddress;
  final int cityId;
  final String password;

  UserData({
    required this.firstName,
    required this.lastName,
    required this.age,
    required this.email,
    required this.phone,
    required this.roleId,
    required this.userAddress,
    required this.cityId,
    required this.password,
  });

  // Méthode pour convertir les données utilisateur en format JSON
  Map<String, dynamic> toJson() {
    return {
      'firstName': firstName,
      'lastName': lastName,
      'age': age,
      'email': email,
      'phone': phone,
      'roleId': roleId,
      'userAddress': userAddress,
      'cityId': cityId,
      'password': password,
    };
  }
}

class InscriptionPage extends StatelessWidget {
  // Contrôleurs pour les champs de texte
  final TextEditingController nomController = TextEditingController();
  final TextEditingController prenomController = TextEditingController();
  final TextEditingController ageController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  final TextEditingController passwordController = TextEditingController();
  final TextEditingController confirmPasswordController =
      TextEditingController();
  final TextEditingController phoneController = TextEditingController();
  final TextEditingController addressController = TextEditingController();
  int? selectedRoleId;
  int? selectedCityId;

  // Liste des rôles et des villes
  final List<Map<String, dynamic>> roles = [
    {'roleId': 1, 'roleName': 'Propriétaire'},
    {'roleId': 2, 'roleName': 'Gardien'},
    {'roleId': 3, 'roleName': 'Les deux'},
  ];

  final List<Map<String, dynamic>> cities = [
    {'cityName': 'Paris', 'cityId': 1},
    {'cityName': 'New York', 'cityId': 2},
    {'cityName': 'London', 'cityId': 3},
  ];

  // Fonctions de validation des champs
  bool validateEmail(String email) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    return emailRegex.hasMatch(email);
  }

  bool validatePhoneNumber(String phoneNumber) {
    return phoneNumber.length == 10 && int.tryParse(phoneNumber) != null;
  }

  bool validateAge(String age) {
    final ageValue = int.tryParse(age);
    return ageValue != null && ageValue >= 18;
  }

  bool validatePassword(String password) {
    return password.length >= 6;
  }

  // Fonction de validation globale des champs
  bool validateFields() {
    return nomController.text.isNotEmpty &&
        prenomController.text.isNotEmpty &&
        ageController.text.isNotEmpty &&
        emailController.text.isNotEmpty &&
        passwordController.text.isNotEmpty &&
        confirmPasswordController.text.isNotEmpty &&
        phoneController.text.isNotEmpty &&
        addressController.text.isNotEmpty &&
        selectedRoleId != null &&
        selectedCityId != null;
  }

  // Fonction pour envoyer les données au serveur
  Future<void> sendData(BuildContext context) async {
    if (!validateFields()) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Veuillez remplir tous les champs.'),
      ));
      return;
    }

    if (!validateEmail(emailController.text)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Veuillez saisir une adresse email valide.'),
      ));
      return;
    }

    if (!validatePhoneNumber(phoneController.text)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Veuillez saisir un numéro de téléphone valide.'),
      ));
      return;
    }

    if (!validateAge(ageController.text)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Vous devez avoir au moins 18 ans pour vous inscrire.'),
      ));
      return;
    }

    if (!validatePassword(passwordController.text)) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Le mot de passe doit contenir au moins 6 caractères.'),
      ));
      return;
    }

    if (passwordController.text != confirmPasswordController.text) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Les mots de passe ne correspondent pas.'),
      ));
      return;
    }

    if (selectedCityId == null) {
      ScaffoldMessenger.of(context).showSnackBar(const SnackBar(
        content: Text('Veuillez sélectionner une ville.'),
      ));
      return;
    }

    final userData = UserData(
      firstName: nomController.text,
      lastName: prenomController.text,
      age: int.parse(ageController.text),
      email: emailController.text,
      phone: phoneController.text,
      roleId: selectedRoleId!,
      userAddress: addressController.text,
      cityId: selectedCityId!,
      password: passwordController.text,
    );

    const url = 'https://api.arosaje.a-hamidi.fr/inscription';
    final response = await http.post(
      Uri.parse(url),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(userData.toJson()),
    );

    if (response.statusCode == 200) {
      Navigator.push(
        context,
        MaterialPageRoute(builder: (context) => LoginPage()),
      );
    } else {
      ScaffoldMessenger.of(context).showSnackBar(SnackBar(
        content: Text('Échec de l\'inscription. Veuillez réessayer.'),
      ));
      print('Échec de l\'inscription. Réponse du serveur: ${response.body}');
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Page d\'Inscription'),
      ),
      body: SingleChildScrollView(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(20.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text(
                  'Inscription',
                  style: TextStyle(
                    fontSize: 24,
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 20),
                TextField(
                  controller: nomController,
                  decoration: const InputDecoration(
                    labelText: 'Nom',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: prenomController,
                  decoration: const InputDecoration(
                    labelText: 'Prénom',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: ageController,
                  decoration: const InputDecoration(
                    labelText: 'Âge',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.number,
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: emailController,
                  decoration: const InputDecoration(
                    labelText: 'Email',
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: passwordController,
                  decoration: const InputDecoration(
                    labelText: 'Mot de passe',
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: confirmPasswordController,
                  decoration: const InputDecoration(
                    labelText: 'Confirmer le mot de passe',
                    border: OutlineInputBorder(),
                  ),
                  obscureText: true,
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: phoneController,
                  decoration: const InputDecoration(
                    labelText: 'Numéro de portable',
                    border: OutlineInputBorder(),
                  ),
                  keyboardType: TextInputType.phone,
                ),
                const SizedBox(height: 10),
                TextField(
                  controller: addressController,
                  decoration: const InputDecoration(
                    labelText: 'Adresse',
                    border: OutlineInputBorder(),
                  ),
                  maxLines: 3,
                ),
                const SizedBox(height: 10),
                DropdownButtonFormField<int>(
                  value: selectedRoleId,
                  decoration: const InputDecoration(
                    labelText: 'Rôle',
                    border: OutlineInputBorder(),
                  ),
                  items: roles.map((role) {
                    return DropdownMenuItem<int>(
                      value: role['roleId'],
                      child: Text(role['roleName']),
                    );
                  }).toList(),
                  onChanged: (value) {
                    selectedRoleId = value;
                  },
                ),
                const SizedBox(height: 10),
                DropdownButtonFormField<int>(
                  value: selectedCityId,
                  decoration: const InputDecoration(
                    labelText: 'Ville',
                    border: OutlineInputBorder(),
                  ),
                  items: cities.map((city) {
                    return DropdownMenuItem<int>(
                      value: city['cityId'],
                      child: Text(city['cityName']),
                    );
                  }).toList(),
                  onChanged: (value) {
                    selectedCityId = value;
                  },
                ),
                const SizedBox(height: 10),
                ElevatedButton(
                  onPressed: () {
                    sendData(context);
                  },
                  child: const Text('S\'inscrire'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
