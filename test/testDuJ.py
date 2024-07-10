import unittest
import json
import requests

class TestFlaskAPI(unittest.TestCase):

    base_url = "https://api.arosaje.a-hamidi.fr"

    def test_inscription_endpoint(self):
        url = self.base_url + "/inscription"
        data = {
            'firstName': 'Jalal',
            'lastName': 'test',
            'email': 'jalal@gmail.com',
            'password': 'password123',
            'phone': '0638048265',
            'userAddress': '123 Main St',
            'roleId': 1,
            'cityId': 1,
            'age': 30
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()

        self.assertIn('status', response_data)
        self.assertEqual(response_data.get('message'), 'inscription OK')

    def test_login_endpoint(self):
        url = self.base_url + "/login"
        data = {
            'email': 'jalal@gmail.com',
            'password': 'password123'
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)
        response_data = response.json()
        print(response_data)

        self.assertIn('token', response_data)
        self.assertEqual(response_data['message'], 'Inscrit')

    def test_addplant_endpoint(self):
        url = self.base_url + "/addplant"
        data = {
            'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjpbbnVsbF0sInVzZXJuYW1lIjoiamFsYWxAZ21haWwuY29tIiwiZXhwIjoxNzIwNjE0MDc5fQ.k6Nm2gBrAFvsibio1CD9p48HkvwBApemzItkuMR0-Jw',  
            'plantDescription': 'A beautiful plant for testing',
            'plantAdress': '456 Park Ave',
            'name': 'Rose',
            'duree_garde': '1 month'
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(url, json=data, headers=headers)

        # Check if the request was successful (status code 2xx)
        self.assertTrue(response.ok, f"Request failed with status code {response.status_code}")

        # Check response content if successful
        if response.ok:
            try:
                response_data = response.json()
                self.assertEqual(response_data.get('message'), 'Plant added successfully')
                # Optionally, you can assert other properties of the response data
            except json.decoder.JSONDecodeError:
                self.fail("Failed to decode response JSON")

if __name__ == "__main__":
    unittest.main()