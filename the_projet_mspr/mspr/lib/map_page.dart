import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';
import 'package:http/http.dart' as http;

// Fonction pour récupérer les coordonnées à partir d'une adresse
Future<LatLng?> getCoordinatesFromAddress(String address) async {
  final url = Uri.parse('http://api.arosaje.a-hamidi.fr/recupererlocalisation');
  final response = await http.get(url);

  if (response.statusCode == 200) {
    final jsonData = json.decode(response.body);
    if (jsonData.isNotEmpty) {
      final location = jsonData[0];
      //on va log la latitude et la longitude
      print('Latitude: ${location['lat']}, Longitude: ${location['lon']}');
      return LatLng(
          double.parse(location['lat']), double.parse(location['lon']));
    }
  }

  return null;
}

Future<Map<String, dynamic>?> getPlantDataFromAPI(String address) async {
  final url = Uri.parse('http://api.arosaje.a-hamidi.fr/recupererlocalisation');
  final response = await http.get(url);

  if (response.statusCode == 200) {
    final jsonData = json.decode(response.body);
    return jsonData;
  }

  return null;
}

String formatDateTime(String dateString) {
  // Analyser la chaîne de date en tant qu'objet DateTime
  DateTime dateTime = DateTime.parse(dateString);

  // Créer une liste des noms de mois
  List<String> monthNames = [
    "",
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre"
  ];

  // Extraire le jour, le mois et l'année de la date
  int day = dateTime.day;
  int month = dateTime.month;
  int year = dateTime.year;
  int hour = dateTime.hour;
  int minute = dateTime.minute;

  // Formater la date dans le format souhaité
  String formattedDate =
      "$day ${monthNames[month]} $year à ${hour.toString().padLeft(2, '0')}:${minute.toString().padLeft(2, '0')}";

  return formattedDate;
}

Future<List<String>?> getAddressesFromAPI() async {}

class MapPage extends StatefulWidget {
  final String pseudo;
  const MapPage({Key? key, required this.pseudo}) : super(key: key);

  @override
  _TrouverPageState createState() => _TrouverPageState();
}

class _TrouverPageState extends State<MapPage> {
  late List<String> _addresses;
  List<Marker> markerList = <Marker>[];

  @override
  void initState() {
    super.initState();
    getAddressesFromAPI().then((addresses) {
      if (addresses != null) {
        setState(() {
          _addresses = addresses;
          print(_addresses);
        });

        Marker createMarker(LatLng latLng, String address) {
          return Marker(
            child: InkWell(
              onTap: () {
                getPlantDataFromAPI(address).then((plantData) {
                  if (plantData != null) {
                    showDialog(
                      context: context,
                      builder: (BuildContext context) {
                        return AlertDialog(
                          title: Text(plantData['nom_plt']),
                          content: Column(
                            mainAxisSize: MainAxisSize.min,
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text('Adresse: ${plantData['adr_plt']}'),
                              Text(
                                  'Date de début: ${formatDateTime(plantData['dat_deb_plt'])}'),
                              Text(
                                  'Date de fin: ${formatDateTime(plantData['dat_fin_plt'])}'),
                              ElevatedButton(
                                child: Text('Garder la plante'),
                                onPressed: () {},
                              ),
                            ],
                          ),
                          actions: <Widget>[
                            TextButton(
                              child: Text('OK'),
                              onPressed: () {
                                Navigator.of(context).pop();
                              },
                            ),
                          ],
                        );
                      },
                    );
                  }
                });
              },
              child: Image.asset('images/plante.png'),
            ),
            width: 80,
            height: 80,
            point: latLng,
          );
        }

        // on va recuperer les coordonnées de chaque adresse puis les afficher sur la carte
        for (final address in _addresses) {
          getCoordinatesFromAddress(address).then((latLng) {
            if (latLng != null) {
              setState(() {
                markerList.add(createMarker(latLng, address));
                // on va afficher les marqueurs sur la carte
                print(markerList);
              });
            }
          });
        }
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "OpenStreetMap Map",
      home: Scaffold(
        body: Stack(
          children: [
            FlutterMap(
              options: MapOptions(
                center: LatLng(45.76, 4.83), // Centre de la carte sur Lyon
                zoom: 13.0,
              ),
              children: [
                TileLayer(
                  urlTemplate:
                      "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                  subdomains: ['a', 'b', 'c'],
                ),
                MarkerLayer(
                  markers: markerList,
                ),
              ],
            ),
            Positioned(
              top: 20,
              left: 10,
              child: IconButton(
                icon: Icon(Icons.arrow_back),
                onPressed: () {
                  Navigator.of(context).pop();
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
