import requests
import json

def login_request(email, password):
    base_url = "https://api.arosaje.a-hamidi.fr"
    url = base_url + "/login"
    data = {
        'email': email,
        'password': password
    }
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an exception for bad response status
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def test_addplant_endpoint():
    base_url = "https://api.arosaje.a-hamidi.fr"
    url = base_url + "/profile"
    data = {
        'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbMV0sInVzZXJuYW1lIjoiamFsYWw1b0BnbWFpbC5jb20iLCJleHAiOjE3MjA2MjY1NDZ9.AVvT9UusgD3P9L-wOjS7cHjq55BgQmoMcnmWlcrQ6Ko',  
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.get(url, json=data, headers=headers)
    response_data = response.json()
    print(response_data)

if __name__ == "__main__":
    test_addplant_endpoint()
    email = 'jalal5o@gmail.com'
    password = 'password123'
    login_response = login_request(email, password)
    if login_response:
        print(login_response)
    else:
        print("Login request failed.")
