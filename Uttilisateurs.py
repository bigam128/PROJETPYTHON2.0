import json


class class_utilisateurs:

    def __init__(self, id, nom, prenom, username, email, mdp, role):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.mdp = mdp
        self.role = role

    @classmethod
    def login(cls, user_file,blackliste_file):
        from Administrateur import Administrateur
        from Etudiant import class_etudiant
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        with open(user_file, "r") as f:
            user_data = json.load(f)
        with open(blackliste_file, "r") as f:
            blackliste_data = json.load(f)
        for user in user_data:
            if user['username'] == username and user['mdp'] == password:
                etudiant_id = user["id"]
                blacklisted = any(x["id"] == etudiant_id for x in blackliste_data)
                if user:
                    if user['role'].lower() == "etudiant":
                        if blacklisted:
                            print("oups!vous etes bloques")
                            return None
                        etudiant_instance = class_etudiant(**user)
                        class_etudiant.user = [etudiant_instance]
                        etudiant_instance.menu_etudiant()  # app etudiant menu
                        return etudiant_instance
                    elif user['role'].lower() == "administrateur":
                        admin_instance = Administrateur(**user)
                        Administrateur.admin=[admin_instance]
                        admin_instance.menu_administrateur()  # app admin menu
                        return admin_instance
        return None