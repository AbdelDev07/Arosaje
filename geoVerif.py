import requests


def adresse_vers_coordonnees(adresse):
    url = f"https://nominatim.openstreetmap.org/search?q={adresse}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return {'lat':latitude, 'long':longitude}
        else:
            return None
    else:
        return None
