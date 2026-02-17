import requests

def url_checker(correct_url):
    file_path= "C:/Users/20221292/Desktop/Projets-1/Python/directories_wordlist.txt"
    based_url= "http://35.175.136.38"
    try:
        with open(file_path, 'r', encoding='ISO-8859-1') as file:
            for i, line in enumerate(file):  # Iterate through the file lines
                word = line.strip()
                test_url= str(based_url+"/"+word)
                print("Testing url: "+str(test_url))
                response = requests.get(test_url, verify=False)
                if response.status_code==200:
                    print(str(test_url)+" is valid\n")
                    correct_url.append(str(test_url))
                else:
                    print(str(test_url)+"URL is invalid\n")
        print("Correct URLs: "+str(correct_url))
    except FileNotFoundError:
        print(f"File not found: {file_path}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

correct_url=[]
url_checker(correct_url)
