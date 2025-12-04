def verifRemise():
    currency= int("Préciser la monaie utilisé (dollar, euro ou pound): ")
    montantAchat= int(input("Indiquez le montant de l'achat: "))        
    if montantAchat >=100 and montantAchat <=500 :
        remise= montantAchat-(montantAchat/20)
        print ("La remise est: ", remise)
    elif montantAchat > 500 :
        remise = montantAchat-((montantAchat/100)*8)
        print ("La remise est: ", remise)
    else : 
        print ("Il n'y a aucune remise")
    

verifRemise()