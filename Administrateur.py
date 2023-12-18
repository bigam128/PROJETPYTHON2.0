import hashlib
from Uttilisateurs import class_utilisateurs
from Etudiant import class_etudiant
from Livre import class_livre
from prettytable import PrettyTable
import json

class Administrateur(class_utilisateurs):
    admin = []

    def __init__(self, id, nom, prenom, username, email, mdp, role):
        super().__init__(id, nom, prenom, username, email, mdp, role)
        self.role = "Administrateur"

    @classmethod
    def affichage_etudiant(cls):  # affichage du tableau en mode pretty table
        table = PrettyTable(['id', 'nom', 'prenom', 'username', 'email', 'mdp','suspended'])
        try:
            with open("listes.json", "r") as f:
                etudiant_data = json.load(f)
                for et_data in etudiant_data:
                    if 'role' in et_data and et_data["role"] == "Etudiant":
                        suspended_status = et_data.get("suspended", False)
                        table.add_row([et_data['id'], et_data['nom'], et_data['prenom'], et_data['username'], et_data['email'], et_data['mdp'], suspended_status])
        except FileNotFoundError:
            print("the file does not exist")
        print(table)

    @classmethod
    def supprimer_livre(cls, livre_id, livre_file):
        if not cls.admin:
            print("Aucun admin connecté.")
            return
        logged_in_etudiant = cls.admin[0]
        with open(livre_file, "r+") as f:
            livres_data = json.load(f)
        filterage_livres = [livre for livre in livres_data if livre["id"] != livre_id]
        with open(livre_file, "w") as f:
            json.dump(filterage_livres, f, indent=2)
        print(f"Livre avec l'ID {livre_id} supprimé")

    @classmethod
    def afficher_etudiant_blacklist(cls, blacklist_file):
        if not cls.admin:
            print("Aucun admin connecté.")
            return
        logged_in_etudiant = cls.admin[0]
        table = PrettyTable(['id', 'username','nom','prenom'])
        with open(blacklist_file, "r") as f:
            etudiant_blacklist = json.load(f)
            for etudiant in etudiant_blacklist:
                table.add_row([etudiant['id'], etudiant['username'], etudiant['nom'], etudiant['prenom']])
        print(table)
    @classmethod
    def supprimer_etudiant(cls,etudiant_id,etudiant_file):
        if not cls.admin:
            print("Aucun admin connecté.")
            return
        logged_in_etudiant = cls.admin[0]
        with open(etudiant_file, "r+") as f:
            etudiant_data = json.load(f)
        filterage_etudiant = [etudiant for etudiant in etudiant_data if etudiant["id"] != etudiant_id]
        with open(etudiant_file, "w") as f:
            json.dump(filterage_etudiant, f, indent=2)
        print(f"Livre avec l'ID {etudiant_id} supprimé")
    @classmethod
    def suspendre_etudiant(cls,etudiant_id, etudiant_file):
        if not cls.admin:
            print("Aucun admin connecté.")
            return
        logged_in_etudiant = cls.admin[0]
        with open(etudiant_file, "r") as f:
            etudiant_data = json.load(f)
        etudiant_exist = any(x['id'] == etudiant_id for x in etudiant_data)
        if etudiant_exist:
            etudiant_info = next(etudiant for etudiant in etudiant_data if etudiant['id'] == etudiant_id)
            print("Etudiant Info:", etudiant_info)

            if cls.ajouter_blacklist(etudiant_info):
                print(f'etudiant avec id {etudiant_id} suspendu ')
            else:
                print(f'etudiant avec id {etudiant_id} deja present dans la liste noire.')
        else:
            print(f'etudiant avec id {etudiant_id} non trouve dans la liste des etudiants.')

    @classmethod
    def ajouter_blacklist(cls, etudiant_info):  # ez
        try:
            with open("blacklist.json", "r") as f:
                blacklist_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            blacklist_data = []
        etudiant_exist = any(x['id'] == etudiant_info['id'] for x in blacklist_data)
        if not etudiant_exist:
            blacklist_data.append({
                'id': etudiant_info['id'],
                'username': etudiant_info['username'],
                'nom': etudiant_info['nom'],
                'prenom': etudiant_info['prenom']
            })
        with open("blacklist.json", "w") as f:
            json.dump(blacklist_data, f, indent=2)
        return not etudiant_exist  # ca retourne true si ajouter dans la liste et false si il est deja dans la liste

    @classmethod
    def reactiver_compte_etudiant(cls, etudiant_id, blacklist_file): #cette metthode est simple vraiment l'administrateur va juste supprimer l'etudiant de la blacklist ett lui donner une chance pour rendre le livre
        if not cls.admin:
            print("Aucun admin connecté.")
            return
        logged_in_etudiant = cls.admin[0]
        with open(blacklist_file,"r") as f:
            blacklist_data = json.load(f)
        filtrage_blacklist = [etudiant for etudiant in blacklist_data if etudiant["id"] != etudiant_id]
        with open(blacklist_file,"w") as f:
            json.dump(filtrage_blacklist,f,indent=2)
        print(f"etudiant avec id {etudiant_id} reactiver")

    @classmethod
    def menu_administrateur(cls):
        print("****************Welcome admin****************")
        while True:
            choix = input("A: Gérer les étudiants \n B: Gérer les livres \n X: Exit \n Saisir votre choix : ")

            if choix.upper() == 'A':
                cls.menu_admin_etudiants()
            elif choix.upper() == 'B':
                cls.menu_admin_livres()
            elif choix.upper() == 'X':
                print("Goodbye!")
                break
            else:
                print("Choix incorrect.")

    def menu_admin_etudiants():
        while True:
            choix_etudiant = input("1: Ajouter un étudiant \n"
                                   "2: Afficher la liste des étudiants \n"
                                   "3: Supprimer un étudiant \n"
                                   "4: Modifier un étudiant \n"
                                   "5: Afficher les étudiants suspendus \n"
                                   "6: Suspendre un compte étudiant \n"
                                   "7: Réactiver un compte étudiant \n"
                                   "0: Revenir au menu principal \n"
                                   "Saisir votre choix : ")

            if choix_etudiant == '1':
                print(class_etudiant.ajouter_user())
            elif choix_etudiant == '2':
                print(Administrateur.affichage_etudiant())
            elif choix_etudiant == '3':
                yy = int(input('Veuillez saisir le ID de l\'étudiant à supprimer : '))
                print(Administrateur.supprimer_etudiant(yy, "listes.json"))
            elif choix_etudiant == '4':
                hh = int(input('Choisir le ID de l\'étudiant que vous voulez modifier : '))
                print(class_etudiant.modifier_etudiant(hh))
            elif choix_etudiant == '5':
                print(Administrateur.afficher_etudiant_blacklist("blacklist.json"))
            elif choix_etudiant == '6':
                t = int(input('veuillez saisir le id : '))
                print(Administrateur.suspendre_etudiant(t, "listes.json"))
            elif choix_etudiant == '7':
                e = int(input('Veuillez saisir le ID de l\'étudiant à réactiver : '))
                print(Administrateur.reactiver_compte_etudiant(e, "blacklist.json"))
            elif choix_etudiant == '0':
                break
            else:
                print("Choix incorrect.")

    def menu_admin_livres():
        while True:
            choix_livre = input("1: Ajouter un livre \n"
                                "2: Afficher les livres avec les emprunts \n"
                                "3: Afficher la liste des livres \n"
                                "4: Supprimer un livre \n"
                                "5: Modifier un livre \n"
                                "0: Revenir au menu principal \n"
                                "Saisir votre choix : ")

            if choix_livre == '1':
                print(class_livre.ajouter_un_livre())
            elif choix_livre == '2':
                print(class_livre.affichage_livres())
            elif choix_livre == '3':
                print(class_livre.affichage_livres_etudiant())
            elif choix_livre == '4':
                l = int(input('Veuillez saisir le ID du livre à supprimer : '))
                print(Administrateur.supprimer_livre(l, "livres.json"))
            elif choix_livre == '5':
                t = int(input('veuillez saisir le ID du livre à modifier : '))
                print(class_livre.modifier_livre(t))
            elif choix_livre == '0':
                break
            else:
                print("Choix incorrect.")

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
