import requests #Il est nécessaire de l'installer via la commande pip install requests

def web_requester(): #Fonction qui effectue une requête web
    url = "https://httpbin.org/get" #URL que l'on utilise pour la requête
    response = requests.get(url, verify=False) #Envoie la requête GET à l'url spécifiée. La vérification SSL est désacivée.
    print(response.status_code) #Affiche le code HTTP
    print(response.headers.get('Server')) #Affiche le type de serveur en utilisant l'entête HTTP 'Server'
    data = response.text #Nécessaire pour récupérer le résultat de la requête
    print(data[:50]) #Affiche les 50 premiers caractères de la réponse

web_requester() #Appelle de la fonction web_requester