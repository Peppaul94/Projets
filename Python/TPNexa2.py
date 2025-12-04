
class Etudiant:
    def __init__(self, nom, prenom, age, sexe, NivPy):
        self.nom= nom 
        self.prenom= prenom 
        self.age= age
        self.sexe= sexe
        self.NivPy= NivPy
        
    def afficher(self):
        print ("Nom: ", self.nom, "\nPrénom: ", self.prenom, "\nÂge: ", self.age, "\nSexe: ", self.sexe, "\nNivPy: ", self.NivPy)

def printListeEtu():
    for i, etu in enumerate(listeEtu, 1):
        print(f"{i}. ", end="")
        etu.afficher()
    
def ajoutEtu(listeEtu, nbEtu):
    nom= input("Veuillez séléctionner le nom du nouvel étudiant: ")
    prenom= input("Veuillez séléctionner le prénom du nouvel étudiant: ")
    age= input("Veuillez séléctionner l'âge du nouvel étudiant: ")
    sexe= input("Veuillez séléctionner le sexe du nouvel étudiant: ")
    NivPy= input("Veuillez séléctionner le niveau du nouvel étudiant: ")
    numNewEtu= nbEtu+1
    idNewEtu= "etu"+ str(numNewEtu)
    listeEtu.append(Etudiant[idNewEtu](nom, prenom, age, sexe, NivPy))
    return listeEtu

def menu(listeEtu, nbEtu):
    print("Bienvenue! Séléctionner une option:\n 1: Afficher la liste des étudiants\n 2: Ajouter un étudiant")
    option=int(input("Votre choix: "))
    if option==1:
        for etu in listeEtu:
            etu.printListeEtu()
    elif option==2:
        ajoutEtu(listeEtu, nbEtu)
    else:
        print("Erreur: veuillez choisir 1 ou 2")
        menu(listeEtu, nbEtu)


listeEtu = {
    "etu1": Etudiant("Havard", "Paul", 22, "Homme", "Experimenté"),
    "etu2": Etudiant("Leblanc", "Dupont", 21, "Homme", "Amateur"),
    "etu3": Etudiant("Lenoir", "Alice", 23, "Femme", "Débutant")
}
nbEtu= len(listeEtu)

menu(listeEtu, nbEtu)


    
    
    

