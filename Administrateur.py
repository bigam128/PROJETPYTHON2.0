import hashlib
from Etudiant import class_etudiant

import Livre
# import Etudiant
from Livre import class_livre
from prettytable import PrettyTable
from tabulate import tabulate
import json


class Administrateur:
    id = 0
    users = []
    @classmethod
    def ajouter_user(cls):
        while True:
            cls.id += 1
            nom = input('Saisir nom : ')
            if nom == "stop":
                break
            prenom = input('Saisir prenom : ')
            username = input('saisir un username : ')
            email = input('Saisir email sous forme (exemple@gmail.com): ')
            mdp = input("Saisir le mot de passe : ")
            confirmer_mdp = input('Confirmer le mot de passe : ')
            if confirmer_mdp == mdp:
                    # Hasher le mot de passe avec MD5
                encrypted = mdp.encode()
                hash_mdp = hashlib.md5(encrypted).hexdigest()
                with open("listes.json", "a") as f:  # Enregistrer les informations dans un fichier txt
                    json.dump([user.__dict__ for user in cls.users], f, indent=2)
                    f.write('\n')
                with open("listes.json", "r") as f3:
                    print(f3.read())
            else:
                print('Veuillez saisir le même mot de passe.')
                return None
            user_instance = class_etudiant(cls.id, nom, prenom, username, email, mdp) #on ajoute les etiduants
            cls.users.append(user_instance)
            for etud in cls.users:
                print(etud.get_usertable_row())

    @classmethod
    def affichage_etudiant(cls):  # affichage du tableau en mode pretty table
        table = PrettyTable(['id', 'nom', 'prenom', 'username', 'email', 'mdp'])
        try:
            with open("listes.json", "r") as f:
                etudiant_data = json.load(f)
                for et_data in etudiant_data:
                    table.add_row([et_data['id'], et_data['nom'], et_data['prenom'], et_data['username'],
                                   et_data['email'], et_data['mdp']])
        except FileNotFoundError:
            print("the file does not exist")
        print(table)


    @classmethod
    def menu_administrateur(cls):
        print("****************Welcome admin****************")
        while True:
            choix = input("""
                        A: ajouter un etudiant 
                        B: ajouter un livre
                        Q: afficher le livre
                        C: afficher mode etudiant
                        D:afficher liste etudiant
                        Please enter your choice: """)
            if choix == 'A':
                print(Administrateur.ajouter_user())

            elif choix == 'B':
                livres = class_livre.ajouter_un_livre()
                for livre in livres:
                    print(livre.get_table_row())

            elif choix == 'Q':
                print(class_livre.affichage_livres())

            elif choix == 'C':
                print(class_livre.affichage_livres_etudiant())

            elif choix == 'D':
                print(Administrateur.affichage_etudiant())

            revenir_menu = input("appuyer sur la touche 0 pour revenir au menu :  ")
            if revenir_menu.lower()==0:
                continue





#Administrateur.menu_administrateur()

# ici on va construire ce que admin va voir


# print(Administrateur.affichage_livres())


# nouveau_etudiant1 = Administrateur.ajouter_user()
# print(nouveau_etudiant1)
# nouveau_livre = class_livre.ajouter_un_livre()
# print(nouveau_livre)


# affichage_livres(nouveau_livre)
# afficher_nouveau_etudiant = Etudiant.afficher_etudiant()
# print(afficher_nouveau_etudiant)
# nouveau_livre = Livre.ajouter_un_livre()
# print(nouveau_livre)
