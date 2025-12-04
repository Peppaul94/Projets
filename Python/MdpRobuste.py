import string

def checkLongueurMdp():
    mdp= input("Entrez votre mot de passe: ")
    tailleMdp= len(mdp)
    if (tailleMdp >= 14):
        print ("Votre mot de passe a une taille correcte")
    elif tailleMdp == 12:
        print ("Votre mot de passe ne respecte pas les recommendations de l'ANSSI mais peut être utilisé")
    else:
        print ("Votre mot de passe n'est pas correcte")
    
checkLongueurMdp()