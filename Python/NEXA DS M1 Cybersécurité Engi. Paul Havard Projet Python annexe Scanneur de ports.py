import socket

# Méthode qui scanne les ports d'une plage d'adresse IP
def scan_port(ip_address, port, end_of_ip, vulnerable_ip):
    # Boucle qui scanne l'entièreté d'une plage d'adresse IP (ici de .1 à .254)
    while end_of_ip <= 135:
        ip=str(ip_address+"."+str(end_of_ip)) # Construction de l'adresse IP avec la bonne syntaxe
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print("Checking: "+str(ip))
                s.settimeout(2)  # Timeout de 2 secondes
                result = s.connect_ex((ip, port)) # Tentative de connexion au port
                # Condition qui vérifie si le port est ouvert
                if result == 0:
                    print(f"The port {port} of {ip} is open")
                    vulnerable_ip.append(ip)
                else:
                    print(f"The port {port} of {ip} is closed or filtered (Result: {result})")
        except Exception as e:
            print(f"Error: {e}")
        end_of_ip+=1
    print("All the IPs with port 22 open: "+str(vulnerable_ip)) # Affiche toutes les adresses IP avec le port 22 ouvert à la fin du script


ip_address = "192.168.65" # Plage d'adresse IP à scanner
port = 22 # Port à scanner
end_of_ip = 130 # Début de la plage d'adresse IP (ici .1)
vulnerable_ip=[] # Liste qui contiendra les adresses IP avec le port scanné ouvert
scan_port(ip_address, port, end_of_ip, vulnerable_ip) # Lancement du script