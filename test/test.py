import json
import unittest
import time
import hashlib
import datetime
import jwt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import sys
sys.path.append(r'C:\Users\user\Downloads\Arosaje-main\Arosaje-main')
from bdd import md5_hash

class TestFlaskAPIWithSelenium(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://localhost:5000")
        self.results = []

    def print_test_result(self, test_name, endpoint, message, status, token):
        print(f"Test: {test_name}")
        print(f"Endpoint: {endpoint}")
        print(f"Message: {message}")
        print(f"Status: {status}")
        print(f"Token: {token}")
        print()

    def test_inscription_endpoint(self):
        driver = self.driver
        driver.get("http://localhost:5000/inscription")

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

        data_json = json.dumps(data)
        script = f'''
        fetch('/inscription', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({data_json})
        }}).then(response => response.json()).then(data => {{
            document.body.innerHTML = JSON.stringify(data);
        }}).catch(error => {{
            document.body.innerHTML = 'Error: ' + error.message;
        }});
        '''
        driver.execute_script(script)

        time.sleep(5)

        element = driver.find_element(By.TAG_NAME, 'body')
        WebDriverWait(driver, 10).until(EC.visibility_of(element))

        response = element.text.strip()
        print("Response:", response)

        response_data = json.loads(response)
        self.assertIn('status', response_data)
        self.assertEqual(response_data.get('message'), 'inscription OK')

        # Pour le test, supprimez la vérification du token
        self.print_test_result('Inscription Endpoint', '/inscription',
                            response_data.get('message', 'N/A'),
                            response_data.get('status', 'N/A'),
                            'N/A')  # Ajusté pour indiquer qu'il n'y a pas de token

        driver.save_screenshot('inscription.png')

    def test_login_endpoint(self):
        driver = self.driver
        driver.get("http://localhost:5000/login")

        data = {
            'email': 'jalal@gmail.com',
            'password': 'password123'
        }

        data_json = json.dumps(data)
        script = f'''
        fetch('/login', {{
            method: 'POST',
            headers: {{
                'Content-Type': 'application/json'
            }},
            body: JSON.stringify({data_json})
        }}).then(response => response.json()).then(data => {{
            document.body.innerHTML = JSON.stringify(data);
        }}).catch(error => {{
            document.body.innerHTML = 'Error: ' + error.message;
        }});
        '''
        driver.execute_script(script)

        time.sleep(5)

        element = driver.find_element(By.TAG_NAME, 'body')
        WebDriverWait(driver, 10).until(EC.visibility_of(element))

        response = element.text.strip()
        print("Response:", response)

        response_data = json.loads(response)
        self.assertIn('token', response_data)
        self.assertEqual(response_data['message'], 'Inscrit')

        self.print_test_result('Login Endpoint', '/login',
                               response_data.get('message', 'N/A'),
                               'Passed',  # Assuming status is always "Passed" if test succeeds
                               response_data.get('token', 'N/A'))

        driver.save_screenshot('login.png')

    def test_generer_jwt(self):
        payload = {'user_id': 123}
        cle_secrete = '689kjLK^%E4mM#'

        jeton = jwt.encode(payload, cle_secrete, algorithm='HS256')

        self.assertIsInstance(jeton, str)

        decoded = jwt.decode(jeton, cle_secrete, algorithms=['HS256'])
        self.assertEqual(decoded['user_id'], 123)

        print("JWT Generation Test Passed")
        print()

    def test_md5_hash(self):
        texte = 'Hello World'
        expected_hash = hashlib.md5(texte.encode('utf-8')).hexdigest()

        result = md5_hash(texte)

        self.assertEqual(result, expected_hash)

        print("MD5 Hash Test Passed")
        print()

    def test_time_token(self):
        temps_debut = datetime.datetime.now()
        delta = datetime.timedelta(hours=3)
        temps_fin = temps_debut + delta

        def time_token():
            return {"debut": temps_debut , "fin": temps_fin}

        result = time_token()

        self.assertIsInstance(result['debut'], datetime.datetime)
        self.assertIsInstance(result['fin'], datetime.datetime)
        self.assertAlmostEqual((result['fin'] - result['debut']), delta, delta=datetime.timedelta(seconds=1))

        print("Time Token Test Passed")
        print()

    # def test_profile_endpoint(self):
    #     driver = self.driver
    #     driver.get("http://localhost:5000/profile")

    #     token = 'votre_token_valide'

    #     data = json.dumps({'token': token})
    #     script = f'''
    #     fetch('/profile', {{
    #         method: 'POST',
    #         headers: {{
    #             'Content-Type': 'application/json'
    #         }},
    #         body: JSON.stringify({data})
    #     }}).then(response => response.text()).then(data => {{
    #         document.body.innerHTML = data;
    #     }}).catch(error => {{
    #         document.body.innerHTML = 'Error: ' + error.message;
    #     }});
    #     '''
    #     driver.execute_script(script)

    #     time.sleep(5)

    #     try:
    #         element = driver.find_element(By.TAG_NAME, 'body')
    #         WebDriverWait(driver, 10).until(EC.visibility_of(element))

    #         response = element.text.strip()
    #         print("Response:", response)

    #         response_data = json.loads(response)
    #         if not response_data:
    #             raise ValueError("Received empty JSON response")

    #         self.assertIn('email', response_data)
    #         self.assertIn('nom', response_data)
    #         self.assertIn('lastname', response_data)
    #         self.assertIn('adresse', response_data)
    #         self.assertIn('ville', response_data)

    #         self.print_test_result('Profile Endpoint', '/profile',
    #                                'N/A',  # No specific message to print here
    #                                'Passed',  # Assuming status is always "Passed" if test succeeds
    #                                'N/A')  # No token in profile endpoint

    #     except NoSuchElementException as e:
    #         self.fail(f"Failed to find element: {str(e)}")
    #     except json.JSONDecodeError as e:
    #         self.fail(f"Failed to decode JSON response: {str(e)}")
    #     except ValueError as e:
    #         self.fail(f"Received empty JSON response: {str(e)}")
    #     except AssertionError as e:
    #         self.fail(f"Assertion error: {str(e)}")
    #     except Exception as e:
    #         self.fail(f"Failed due to unexpected error: {str(e)}")

    #     driver.save_screenshot('profile.png')

    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()