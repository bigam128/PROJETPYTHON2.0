import json
from Livre import class_livre

class class_etudiant:
    user = []

    def __init__(self, id, nom, prenom, username, email, mdp):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.mdp = mdp
        self.livres_empruntes = []

    def get_usertable_row(self):
        return [self.id, self.nom, self.prenom, self.username, self.email, self.mdp]

    @classmethod
    def login(cls, username, password):  # login pour etudiant
        with open("listes.json", "r") as f:
            users_data = json.load(f)
        for user_data in users_data:
            if user_data["username"] == username and user_data["mdp"] == password:
                return True
        return False

    @classmethod
    def emprunter_livre(cls, livre_id, livres_file):
        with open(livres_file, "r") as f:
            lv = json.load(f)
        livre = next((livre for livre in lv if livre['id'] == livre_id and livre['nbr_exemplaire'] > 0), None)
        if livre:
            livre['nbr_exemplaire'] -= 1
            with open(livres_file, "w") as f:
                json.dump(lv, f,indent=2)
                print(f"livre '{livre['titre']}' emprunter")
        else:
                print("error")
    @classmethod
    def affiche_emprunts(cls, etudiant_id, livres_file):
        if not cls.user:
            print("acun etudiant connecte")
            return
        logged_in_etudiant = cls.user[0]
        with open(livres_file, "r") as f:
            livres_data = json.load(f)
        #emprunts = [livre for livre in livres_data if ]
            #if not emprunts:
                #print(f"emprunts de etudiant {etudiant_id}")
                #for emprunt in emprunts:
                #print(f"id: {emprunt['id']}, Titre: {emprunt['titre']}")
                #else:
                    #print(f'nas de livre  pour letud {etudiant_id}')

            #else:
                #print(" pas de id")

    @classmethod
    def menu_etudiant(cls):
        print("****************Welcome etudiant****************")
        username = input("enter your username")
        password = input("enter your password: ")
        logged_in = cls.login(username,password)
        if logged_in:
            while True:
                choix = input("""
                                A: emprenter livre
                                B: afficher mode etudiant
                                C: afficher empreintts
                                D:
                                Please enter your choice: """)
                if choix == 'A':
                    l = int(input('choisir le id :'))
                    print(class_etudiant.emprunter_livre(l, "livres.json"))
                elif choix == 'B':
                    print(class_livre.affichage_livres_etudiant())

#class_etudiant.menu_etudiant()
#print(class_etudiant.emprunter_livre(1,"livres.json"))
#print(class_etudiant.affiche_emprunts(1, "listes.json"))







#us = input("enter your username")
#pas = input("entter your password")
#if class_etudiant.login(us, pas):
    #print("login successful")
#else:
    #print("invalid")
