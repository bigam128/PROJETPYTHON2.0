import json
from Uttilisateurs import class_utilisateurs
from prettytable import PrettyTable
from Livre import class_livre
from datetime import datetime
import hashlib

class class_etudiant(class_utilisateurs):
    user = []
    #logged_in_etudiant = None

    def __init__(self, id, nom, prenom, username, email, mdp, role, livres_empruntes=None, suspended=False):
        super().__init__(id, nom, prenom, username, email, mdp, role)
        self.livres_empruntes = livres_empruntes if livres_empruntes is not None else []
        self.suspended = suspended
        self.role = "Etudiant"

    @classmethod
    def ajouter_user(cls):
        try:
            with open("listes.json", "r") as f:
                cls.user = json.load(f)
        except(FileNotFoundError,
               json.JSONDecodeError):  # ca ca ca n'as pas voulu ouvrir le fichier quand j'ai ecris juste FileNot found error
            cls.user = []
        max_id = max(cls.user, key=lambda x: x['id'], default={'id': 0}).get(
            'id')  # trouver le id max dans la liste key lambda x(element comme livres[...]) fonction pour qui va rendre la valeur id
        nouv_id = int(max_id) + 1  # on ajoute le id depending on the previous id ce qui le MAX!!!
        while True:
            nom = input('Saisir nom : ')
            if nom == "stop":
                break
            prenom = input('Saisir prenom : ')
            username = input('saisir un username : ')
            if any(user.get('username') == username for user in cls.user):
                print('username doit être unique. Veuillez choisir un autre username.')
                continue
            email = input('Saisir email sous forme (exemple@gmail.com): ')
            mdp = input("Saisir le mot de passe : ")
            confirmer_mdp = input('Confirmer le mot de passe : ')
            if confirmer_mdp == mdp:
                # hasher le mot de passe avec MD5 pq pas
                encrypted = mdp.encode()
                hash_mdp = hashlib.md5(encrypted).hexdigest()
                user_instance = class_etudiant(nouv_id, nom, prenom, username, email, mdp,role=None)  # on ajoute les etiduants
                user_data = user_instance.__dict__
                user_data["livres_empruntes"] = user_instance.livres_empruntes
                user_data["suspended"] = user_instance.suspended
                user_data["role"]= user_instance.role
                cls.user.append(user_data)
                with open("listes.json", "w") as f:  # Enregistrer les informations dans un fichier json
                    json.dump(cls.user, f, indent=2)
                    f.write('\n')
                print(user_data)
                nouv_id += 1
            else:
                print('Veuillez saisir le même mot de passe.')

    def get_usertable_row(self):
        return [self.id, self.nom, self.prenom, self.username, self.email, self.mdp, self.livres_empruntes,self.suspended]


    @classmethod
    def emprunter_livre(cls, livre_id, livres_file, etudiants_file): #mdm
        if not cls.user:
            print("Aucun étudiant connecté.")
            return
        logged_in_etudiant = cls.user[0]
        if len(logged_in_etudiant.livres_empruntes) >= 3: #!!!!!!!!!
            print("vous avez atteint le max.")
            return False
        if class_livre.emprunter_livre(livre_id, logged_in_etudiant.id, livres_file):
            with open(etudiants_file, "r") as f:
                etudiants_data = json.load(f)
            for etudiant_data in etudiants_data: #trouver si l'etudiant est logged_in pour avoir son id
                if etudiant_data["id"] == logged_in_etudiant.id:
                    if etudiant_data["livres_empruntes"] is None:
                        etudiant_data["livres_empruntes"] = [livre_id]
                    else:
                        etudiant_data["livres_empruntes"].append(livre_id)
            with open(etudiants_file, "w") as f:
                json.dump(etudiants_data, f, indent=2)
            print(f" livre avec le id {livre_id} emprunter")
        else:
            print(f"Le livre avec le id {livre_id} n'est pas disponible.")
    @classmethod
    def affiche_emprunts(cls, livre_file, etudiants_file): #harddddd
        from Administrateur import Administrateur # ca va nous servir pour ajouter_blacklist mais apres je pense je vais changer la methode!!
        if not cls.user:
            print("acun etudiant connecte")
            return
        logged_in_etudiant = cls.user[0] #etudiant connecte
        with open(livre_file, "r") as f:
            livres_data = json.load(f)
        with open(etudiants_file) as f:
            etudiant_data = json.load(f)
        for etudiant_data in etudiant_data:
            etudiant_id = etudiant_data["id"]
            if etudiant_id == logged_in_etudiant.id:
                livres_empruntes = etudiant_data.get("livres_empruntes", [])
                if livres_empruntes:
                    table = PrettyTable(['id', 'titre', 'auteur', 'Date emprunt', 'jours countdown'])
                    for liv_id in livres_empruntes:
                        #print("liv_id:", liv_id) pour debbbogage!!
                        livre = next((livre for livre in livres_data if livre['id'] == liv_id), None)
                        if livre and 'date_emprunt' in livre:
                            date_emprunt_list = livre['date_emprunt']
                                #print("date_emprunt_list:", date_emprunt_list) pour debbbogage!!
                            for info in date_emprunt_list:
                                if info['etudiant_id'] == etudiant_id: # ici pour verifier si le id est le meme et donner le meme id dans la liste
                                    date_emprunt = datetime.strptime(info['date_emprunt'], "%Y-%m-%d %H:%M:%S")
                                    #print("date_emprunt:", date_emprunt) pour debbbogage!!
                                    jours_ctdwn = (datetime.now() - date_emprunt).days
                                    #print("jours_ctdwn:", jours_ctdwn) pour debbbogage!!
                                    if jours_ctdwn > 7:
                                        Administrateur.ajouter_blacklist({ #ou bien je peux juste enlever ca d'ici et suspendre l'etudiant de Administrateur sans utiliser cette methode ici mais ca marche aussi
                                            'id': logged_in_etudiant.id,
                                            'username': logged_in_etudiant.username,
                                            'nom': logged_in_etudiant.nom,
                                            'prenom': logged_in_etudiant.prenom
                                        })
                                    table.add_row([livre['id'], livre['titre'], livre['auteur'], date_emprunt, jours_ctdwn])
                    print(table)
                else:
                    print('aucun livre emprunte.')
                break
        else:
            print('aucun utilisateur trouve.')

    @classmethod
    def supprimer_emprunt(cls,livre_id , etudiant_file, livres_file): # pourquoi ca supprime touts les emprunts?
        if not cls.user:
            print("aucun etudiant connecte")
            return
        logged_in_etudiant = cls.user[0] #j'avais ecris que [0] au debut mais ca a donner error
        with open(etudiant_file, "r") as f:
            etudiant_data = json.load(f)
        for idx, etudiant in enumerate(etudiant_data):
            if etudiant["id"] == logged_in_etudiant.id:
                livres_empruntes = etudiant["livres_empruntes"]
                if livre_id in livres_empruntes:
                    livres_empruntes.remove(livre_id)
                    class_livre.supp_emprunt(logged_in_etudiant.id,livre_id, livres_file)
                    with open(etudiant_file, "w") as f:
                        json.dump(etudiant_data, f, indent=2)
                    #///// incrementer le nbr exemplaire !
                    with open(livres_file, "r") as f:
                        livres_data = json.load(f)
                    for livre in livres_data:
                        if livre["id"] == livre_id:
                            livre["nbr_exemplaire"] += 1 #retourner
                            with open(livres_file, "w") as f_updt:
                                json.dump(livres_data, f_updt, indent=2)
                            print(f"livre avec id {livre_id} retourner")
                            return
        print("aucun livre correspendant avec cet id")

    @classmethod
    def modifier_etudiant(cls, etudiant_id, new_username=None, new_nom=None, new_prenom=None, new_email=None):
        try:
            with open("listes.json", "r") as f:
                etudiant_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading student data.")
            return

        etudiant_exist = any(x['id'] == etudiant_id for x in etudiant_data)
        if etudiant_exist:
            print(f"Choisissez les modifications pour l'étudiant avec ID {etudiant_id}:")
            print("1. Changer le nom")
            print("2. Changer le prénom")
            print("3. Changer l'email")
            print("4. Changer le nom d'utilisateur")
            print("5. Quitter sans modifications")

            choix_modification = input("Choix : ")

            if choix_modification == '1':
                new_nom = input("Nouveau nom: ")
            elif choix_modification == '2':
                new_prenom = input("Nouveau prénom: ")
            elif choix_modification == '3':
                new_email = input("Nouvel email: ")
            elif choix_modification == '4':
                new_username = input("Nouveau nom d'utilisateur: ")
            elif choix_modification == '5':
                print("Quitter sans modifications.")
                return

            for etudiant in etudiant_data:
                if etudiant['id'] == etudiant_id:
                    if new_username is not None:
                        etudiant['username'] = new_username
                    if new_nom is not None:
                        etudiant['nom'] = new_nom
                    if new_prenom is not None:
                        etudiant['prenom'] = new_prenom
                    if new_email is not None:
                        etudiant['email'] = new_email

            with open("listes.json", "w") as f:
                json.dump(etudiant_data, f, indent=2)
                print(f"Étudiant avec ID {etudiant_id} modifié avec succès.")
        else:
            print(f"Aucun étudiant trouvé avec l'ID {etudiant_id}.")
    @classmethod
    def menu_etudiant(cls): #ez
        print("****************Welcome etudiant****************")
        while True:
            choix = input(" A: emprunter un livre \n B: afficher la liste des livres disponible\n C: afficher empreints\n D: retourner un livre \nX:Retourner\n saisir votre choix : ")
            if choix == 'A':
                l = int(input('choisir le id :'))
                print(class_etudiant.emprunter_livre(l, "livres.json", "listes.json"))
            elif choix == 'B':
                print(class_livre.affichage_livres_etudiant())
            elif choix == 'C':
                print(class_etudiant.affiche_emprunts("livres.json", "listes.json"))
            elif choix == 'D':
                l = int(input("veuillez saisir id : "))
                print(class_etudiant.supprimer_emprunt(l,"listes.json", "livres.json"))
            elif choix == 'X':
                return



if __name__ == "__main__":
    logged_in_user = class_utilisateurs.login("listes.json","blacklist.json")

#class_etudiant.menu_etudiant()
#print(class_etudiant.emprunter_livre(1,"livres.json"))
#print(class_etudiant.affiche_emprunts(1, "listes.json"))







#us = input("enter your username")
#pas = input("entter your password")
#if class_etudiant.login(us, pas):
    #print("login successful")
#else:
    #print("invalid")
