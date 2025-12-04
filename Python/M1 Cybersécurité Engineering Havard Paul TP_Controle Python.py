import hashlib
from datetime import datetime

class User: # Définition de la classe User avec 5 attributs: username, password_hash (un mot de passe haché pour plus de sécurité), role (admin ou user), is_blocked (pour bloquer un utilisateur après trop de tentatives échouées), failed_attempts (compteur de tentatives échouées)
    def __init__(self, username, role="user"):
        self.username = username
        self.password_hash = None
        self.role = role
        self.is_blocked = False
        self.failed_attempts = 0

    def set_password(self, password): # Hachage du mot de passe (SHA-256)
        self.password_hash = hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password): # Vérification du mot de passe
        if self.password_hash is None:
            return False
        return self.password_hash == hashlib.sha256(password.encode()).hexdigest()

    def block_user(self): # Bloque l'utilisateur après 3 tentatives échouées
        self.is_blocked = True

    def reset_failed_attempts(self): # Réinitialise le compteur de tentatives échouées
        self.failed_attempts = 0

    def unlock(self): # Débloque un utilisateur donné (uniquement possible en tant qu'administrateur)
        self.is_blocked = False
        self.failed_attempts = 0

class AuthSystem: # Définition de la classe AuthSystem qui gère la connexion des utilisateurs et tout ce qui en découle
    def __init__(self): # Initialise les utilisateurs et les logs
        self.users = {}
        self.logs = []

    def log_event(self, message): # Enregistre les événements dans un journal d'événement visible par un administrateur uniquement
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"[{timestamp}] {message}")

    def register_user(self, username, password, role="user"): # Enregistre un nouvel utilisateur avec un nom d'utilisateur et un mot de passe. Par défaut, son rôle est "user"
        if username in self.users:
            self.log_event(f"Registration failed: {username} already exists.")
            return False
        user = User(username, role)
        user.set_password(password)
        self.users[username] = user
        self.log_event(f"User registered: {username} ({role})")
        return True

    def authenticate(self, username, password): # Méthode d'authentification
        user = self.users.get(username)
        if not user:
            self.log_event(f"Authentication failed: {username} does not exist.")
            print("Erreur de connexion: vérifiez vos identifiants.")
            return False
        elif user.is_blocked:
            self.log_event(f"Authentication blocked: {username} account is blocked.")
            print("Erreur de connexion: votre compte est bloqué.")
            return False
        elif user.verify_password(password):
            user.reset_failed_attempts()
            print("Bienvenue", username +"!")
            self.log_event(f"Authentication success: {username}")
            return True
        else:
            user.failed_attempts += 1
            print("Erreur de connexion: Vérifiez vos identifiants.")
            self.log_event(f"Authentication failed: {username} (attempt {user.failed_attempts})")
            if user.failed_attempts >= 3:
                user.block_user()
                print ("Compte bloqué: Votre compte a été bloqué suite à plusieurs tentatives échouées.")
                self.log_event(f"Account blocked: {username} after 3 failed attempts.")
            return False

    def show_users(self): # Affiche les utilisateurs (uniquement accessible par un administrateur)
        print("Users:")
        for user in self.users.values():
            print(f"- {user.username} ({user.role}){' [BLOCKED]' if user.is_blocked else ''}")

    def show_logs(self): # Affiche le journal d'événements (uniquement accessible par un administrateur)
        print("Security Logs:")
        for log in self.logs:
            print(log)
    
    def connexion(self): # Méthode de connexion
        print ("\n-- Connexion de l'utilisateur --")
        username=input("Entrez le nom d'utilisateur: ")
        password=input("Entrez le mot de passe (indice: tapez mot de passe en anglais pour alice. Mot de passe admin: 'admin123'): ")
        success=auth.authenticate(username, password)
        return success, username
    
    def menu_admin(self): # Menu de l'administrateur accessible une fois les scénarios principaux complétés. Ceci sert de bonus.
        print("\n--- Menu administrateur ---")
        print ("\nVeuillez séléctionner l'une de ces options: ")
        print("1. Afficher les utilisateurs")
        print("2. Afficher les logs de sécurité")
        print("3. Réinitialiser le mot de passe d'un utilisateur")
        print("4. Débloquer un utilisateur")
        print("5. Retourner à la page de connexion")
        print("6. Création d'un nouvel utilisateur")
        print("0. Fermer le programme")
        choice= input("Votre choix: ")
        if choice== "1":
            auth.show_users()
            self.menu_admin()
        elif choice == "2":
            auth.show_logs()
            self.menu_admin()
        elif choice == "3":
            admin_password = input("Entrez votre mot de passe administrateur: ")
            username = input("Entrez le nom d'utilisateur à réinistialiser: ")
            new_password = input("Entrez le nouveau mot de passe: ")
            if auth.reset_password(admin_password, username, new_password):
                print(f"Mot de passe de {username} réinitialiser avec succès.")
                self.menu_admin()
            else:
                print("Echec de la réinitialisation du mot de passe.")
                self.menu_admin()
        elif choice == "4":
            print("\n Liste des utilisateurs: ")
            auth.show_users()
            admin_password = input("Entrez votre mot de passe administrateur: ")
            username = input("Entrez le nom d'utilisateur à débloquer: ")
            if auth.unlock_user(admin_password, username):
                print(f"Utilisateur {username} débloqué avec succès.")
                self.menu_admin()
            else:
                print("Echec du déblocage de l'utilisateur.")
                self.menu_admin()
        elif choice == "5":
            print("Au revoir!")
            auth.log_event("Administrator left the application.")
            auth.connexion_bonus()
        elif choice == "6":
            new_username = input("Entrez le nom d'utilisateur du nouvel utilisateur: ")
            new_password = input("Entrez le mot de passe du nouvel utilisateur: ")
            if self.register_user(new_username, new_password):
                print(f"Utilisateur {new_username} créé avec succès.")
            else:
                print("Echec de la création de l'utilisateur.")
            self.menu_admin()
        elif choice == "0":
            print("Fermeture du programme en cours...")
            auth.log_event("Application closed by user.")
            exit()
        else:
            print("Choix invalide, veuillez entrer l'une des options proposées.")
            self.menu_admin()
        
    def connexion_bonus(self): #Méthode de connexion bonus accessible une fois les scénarios principaux complétés.
        print ("\n-- Connexion de l'utilisateur --")
        print ("\n(Pour quitter le programme, taper 'exit' comme nom d'utilisateur)")
        username=input("Entrez le nom d'utilisateur: ")
        password=input("Entrez le mot de passe (indice: tapez mot de passe en anglais): ")
        success= auth.authenticate(username, password)
        if success is True and username =="admin" and auth.users["admin"].is_blocked is False:
            self.menu_admin()
        elif success is True and username !="admin":
            print("Bravo! Vous avez compléter tous les scénarios! Vous pouvez quitter le programme en tapant 'exit' comme nom d'utilisateur.")
            self.connexion_bonus()
        elif username == "exit":
            print("Fermeture du programme en cours...")
            auth.log_event("Application closed by user.")
            exit()
        else:
            print("Identifiants invalides ou compte bloqué. Veuillez réessayer.")
            self.connexion_bonus()

    # Bonus: Reset password (admin only)
    def reset_password(self, admin_password, username, new_password):
        admin = self.users.get("admin")
        if not admin or not admin.verify_password(admin_password):
            self.log_event(f"Password reset failed: mauvais mot de passe admin.")
            return False
        user = self.users.get(username)
        if not user:
            self.log_event(f"Password reset failed: {username} does not exist.")
            return False
        user.set_password(new_password)
        user.reset_failed_attempts()
        user.is_blocked = False
        self.log_event(f"Password reset: {username} by admin Administrator")
        return True

    # Bonus: Unlock user (admin only)
    def unlock_user(self, admin_password, username):
        admin = self.users.get("admin")
        if not admin or not admin.verify_password(admin_password):
            self.log_event(f"Password reset failed: mauvais mot de passe admin.")
            return False
        user = self.users.get(username)
        if not admin or admin.role != "admin":
            self.log_event(f"Unlock failed: {admin_password} is not admin.")
            return False
        if not user:
            self.log_event(f"Unlock failed: {username} does not exist.")
            return False
        user.unlock()
        self.log_event(f"Account unlocked: {username} by admin")
        return True

# Programme principal
if __name__ == "__main__":
    auth = AuthSystem()
    print("Bienvenue dans le système d'authentification sécurisé.\n")
    # Ajout des utilisateurs
    auth.register_user("admin", "admin123", role="admin")
    auth.register_user("alice", "password", role="user")

    scé_1 =True
    scé_2 = False
    scé_3 = False
    scé_4= False
    # Simulations de connexions
    print("\n--- Scénario 1: Alice se connecte correctement ---")
    
    while scé_1:
        scénario_complet, who = auth.connexion()
        if scénario_complet is True and who == "alice" and not auth.users["alice"].is_blocked:
            print("Scénario complété")
            scé_1 = False
            scé_2 = True
        elif scénario_complet is False or not who == "alice":
            print("(Veuillez respecter le scénario)")
        elif auth.users["alice"].is_blocked:
            print("Dûe à un nombre trop élevé de tentatives échouées, le compte alice a été bloqué. Pour avancer dans les scénarios, veillez relancer le programme (ctrl+c pour sortir du programme).")
        else:
            print("Erreur inattendue")

    print("\n--- Scénario 2: Alice se trompe 3 fois ---")
    échec = 0
    while scé_2:
        scénario_complet, who = auth.connexion()
        if scénario_complet is True:
            print("(Veuillez respecter le scénario)")
        elif scénario_complet is False and who == "alice":
            échec += 1
            if échec == 3:
                print("Scénario complété")
                scé_2 = False
                scé_3 = True
        elif who != "alice":
            print("(Veuillez respecter le scénario)")
        else:
            print("Erreur inattendue")

    print("\n--- Scénario 3: L'admin se connecte correctement ---")
    while scé_3:
        scénario_complet, who = auth.connexion()
        if scénario_complet is True and who == "admin":
            print("Scénario complété")
            print("\n --- Fin des scénarios principaux ---")
            auth.menu_admin()
        elif scénario_complet is False or who != "admin":
            print("(Veuillez respecter le scénario)")
        else:
            print("Erreur inattendue")

     

    