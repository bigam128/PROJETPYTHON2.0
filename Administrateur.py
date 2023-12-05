import hashlib
from Etudiant import class_etudiant
from Livre import class_livre
from prettytable import PrettyTable
import json

class Administrateur:
    id = 0
    users = []
    @classmethod
    def ajouter_user(cls):
        try:
            with open("listes.json", "r") as f:
                cls.users = json.load(f)
        except(FileNotFoundError,json.JSONDecodeError):  # ca ca ca n'as pas voulu ouvrir le fichier quand j'ai ecris juste FileNot found error
            cls.users = []
        max_id = max(cls.users, key=lambda x: x['id'], default={'id': 0}).get('id')  # trouver le id max dans la liste key lambda x(element comme livres[...]) fonction pour qui va rendre la valeur id
        nouv_id = int(max_id) + 1  # on ajoute le id depending on the previous id ce qui le MAX!!!
        while True:
            nom = input('Saisir nom : ')
            if nom == "stop":
                break
            prenom = input('Saisir prenom : ')
            username = input('saisir un username : ')
            if any(user.get('username') == username for user in cls.users):
                print('username doit être unique. Veuillez choisir un autre username.')
                continue
            email = input('Saisir email sous forme (exemple@gmail.com): ')
            mdp = input("Saisir le mot de passe : ")
            confirmer_mdp = input('Confirmer le mot de passe : ')
            if confirmer_mdp == mdp:
                #hasher le mot de passe avec MD5 pq pas
                encrypted = mdp.encode()
                hash_mdp = hashlib.md5(encrypted).hexdigest()
                user_instance = class_etudiant(nouv_id, nom, prenom, username, email, mdp,livres_empruntes=None,suspended=False)  # on ajoute les etiduants
                cls.users.append(user_instance.__dict__)
                with open("listes.json", "w") as f:  # Enregistrer les informations dans un fichier json
                    json.dump(cls.users, f, indent=2)
                    f.write('\n')
                print(user_instance)
                nouv_id+=1
            else:
                print('Veuillez saisir le même mot de passe.')


    @classmethod
    def affichage_etudiant(cls):  # affichage du tableau en mode pretty table
        table = PrettyTable(['id', 'nom', 'prenom', 'username', 'email', 'mdp','suspended'])
        try:
            with open("listes.json", "r") as f:
                etudiant_data = json.load(f)
                for et_data in etudiant_data:
                    table.add_row([et_data['id'], et_data['nom'], et_data['prenom'], et_data['username'],
                                   et_data['email'], et_data['mdp'], et_data["suspended"]])
        except FileNotFoundError:
            print("the file does not exist")
        print(table)

    @classmethod
    def supprimer_livre(cls, livre_id, livre_file):
        with open(livre_file, "r+") as f:
            livres_data = json.load(f)
        filterage_livres = [livre for livre in livres_data if livre["id"] != livre_id]
        with open(livre_file, "w") as f:
            json.dump(filterage_livres, f, indent=2)
        print(f"Livre avec l'ID {livre_id} supprimé")
   # @classmethod
    #def supprimer_etudiant(cls,etudiant_id, etudiant_file):

    @classmethod
    def afficher_etudiant_blacklist(cls, blacklist_file):
        table = PrettyTable(['id', 'username','nom','prenom'])
        with open(blacklist_file, "r") as f:
            etudiant_blacklist = json.load(f)
            for etudiant in etudiant_blacklist:
                table.add_row([etudiant['id'], etudiant['username'], etudiant['nom'], etudiant['prenom']])
        print(table)
    @classmethod
    def supprimer_etudiant(cls,etudiant_id,etudiant_file):
        with open(etudiant_file, "r+") as f:
            etudiant_data = json.load(f)
        filterage_etudiant = [etudiant for etudiant in etudiant_data if etudiant["id"] != etudiant_id]
        with open(etudiant_file, "w") as f:
            json.dump(filterage_etudiant, f, indent=2)
        print(f"Livre avec l'ID {etudiant_id} supprimé")
    @classmethod
    def suspendre_etudiant(cls,etudiant_id, etudiant_file):
        with open(etudiant_file, "r") as f:
            etudiant_data = json.load(f)
        etudiant_exist = any(x['id'] == etudiant_id for x in etudiant_data)
        if etudiant_exist:
            etudiant_info = next(etudiant for etudiant in etudiant_data if etudiant['id'] == etudiant_id)
            print("Etudiant Info:", etudiant_info)

            if cls.ajouter_blacklist(etudiant_info):
                print(f'Etudiant avec ID {etudiant_id} suspendu et ajouté à la liste noire.')
            else:
                print(f'Etudiant avec ID {etudiant_id} déjà présent dans la liste noire.')
        else:
            print(f'Etudiant avec ID {etudiant_id} non trouvé dans le fichier des étudiants.')

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
            choix = input("A: ajouter un etudiant \n B: ajouter un livre \n C: afficher les livres avec les emprunts \n D: afficher la liste des livres \n E:afficher liste etudiant \n F:suprrimer un livre\n G:afficher les etudiant suspendu \n H:reactiver un compte etudiant\n I:suspendre etudiant \n J:supprimer etudiant \nX:exit \n saisir votre choix : ")
            if choix == 'A':
                print(Administrateur.ajouter_user())
            elif choix == 'B':
                print(class_livre.ajouter_un_livre())
            elif choix == 'C':
                print(class_livre.affichage_livres())
            elif choix == 'D':
                print(class_livre.affichage_livres_etudiant())
            elif choix == 'E':
                print(Administrateur.affichage_etudiant())
            elif choix == 'F':
                l = int(input('veuillez saisir le id : '))
                print(Administrateur.supprimer_livre(l,"livres.json"))
            elif choix == 'G':
                print(Administrateur.afficher_etudiant_blacklist("blacklist.json"))
            elif choix == 'H':
                e = int(input('veuillez saisir le id : '))
                print(Administrateur.reactiver_compte_etudiant(e, "blacklist.json"))
            elif choix == 'I':
                t = int(input('veuillez saisir le id : '))
                print(Administrateur.suspendre_etudiant(t,"listes.json"))
            elif choix == 'J':
                yy = int(input('veuillez saisir le id : '))
                print(Administrateur.supprimer_etudiant(yy,"listes.json"))
            elif choix == 'X':
                return
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
