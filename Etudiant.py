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
        self.livres_empruntes = [] if livres_empruntes is not None else livres_empruntes
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
                user_instance = class_etudiant(nouv_id, nom, prenom, username, email, mdp, role=None)  # on ajoute les etiduants
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
    def emprunter_livre(cls, livre_id, livres_file, etudiants_file, redlist_file): #mdm
        if not cls.user:
            print("Aucun étudiant connecté.")
            return
        logged_in_etudiant = cls.user[0]
        num_books_borrowed = logged_in_etudiant.nombre_livre(etudiants_file)
        print(f"numero de livre empreinter: {num_books_borrowed} !")

        if num_books_borrowed >= 3:
            print("Vous avez atteint le maximum d'emprunts (3 livres).")
            return
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
            #cls.verifier_emprunts_en_retard(etudiants_file, livres_file, redlist_file)
            cls.user[0].livres_empruntes = etudiants_data[0].get("livres_empruntes", [])
            print(f" livre avec le id {livre_id} emprunter")
        else:
            print(f"Le livre avec le id {livre_id} n'est pas disponible.")

    def nombre_livre(self, etudiants_file):
        with open(etudiants_file, "r") as f:
            etudiants_data = json.load(f)
        etudiant_info = next((etudiant for etudiant in etudiants_data if etudiant["id"] == self.id), None)
        if etudiant_info:
            return len(etudiant_info.get("livres_empruntes", []))
        else:
            return 0
    @classmethod
    def affiche_emprunts(cls, livre_file, etudiants_file): #harddddd

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
                                    table.add_row([livre['id'], livre['titre'], livre['auteur'], date_emprunt, jours_ctdwn])
                    print(table)
                else:
                    print('aucun livre emprunte.')
                break
        else:
            print('aucun utilisateur trouve.')

    @classmethod
    def supprimer_emprunt(cls,livre_id , etudiant_file, livres_file,redlist_file): # pourquoi ca supprime touts les emprunts?
        if not cls.user:
            print("Aucun étudiant connecté.")
            return

        logged_in_etudiant = cls.user[0]

        with open(etudiant_file, "r") as f:
            etudiant_data = json.load(f)

        for idx, etudiant in enumerate(etudiant_data):
            if etudiant["id"] == logged_in_etudiant.id:
                livres_empruntes = etudiant["livres_empruntes"]
                if livre_id in livres_empruntes:

                    redlist_data = cls.lire_redlist(redlist_file)
                    livre_depasse = False
                    for redlist_etudiant in redlist_data:
                        if (
                                redlist_etudiant.get("id") == logged_in_etudiant.id
                                and "livres_empruntes" in redlist_etudiant
                                and livre_id in redlist_etudiant["livres_empruntes"]
                        ):

                            book_overdue = True
                            break

                    livres_empruntes.remove(livre_id)
                    class_livre.supp_emprunt(logged_in_etudiant.id, livre_id, livres_file)

                    if livre_depasse:
                        cls.retirer_redlist(etudiant["id"], livre_id, redlist_file)
                    with open(etudiant_file, "w") as f:
                        json.dump(etudiant_data, f, indent=2)
                    with open(livres_file, "r") as f:
                        livres_data = json.load(f)
                    for livre in livres_data:
                        if livre["id"] == livre_id:
                            livre["nbr_exemplaire"] += 1
                            with open(livres_file, "w") as f_updt:
                                json.dump(livres_data, f_updt, indent=2)
                            print(f"Livre avec ID {livre_id} retourné avec succès.")
                            return
        print("Aucun livre correspondant avec cet ID.")

    @classmethod
    def lire_redlist(cls, redlist_file):
        try:
            with open(redlist_file, "r") as f:
                redlist_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            redlist_data = []

        return redlist_data

    @classmethod
    def afficher_etudiants_redlist(cls, redlist_file, etudiants_file, livres_file):
        try:
            with open(redlist_file, "r") as f:
                redlist_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors de la lecture de la liste rouge.")
            return

        try:
            with open(etudiants_file, "r") as f:
                etudiants_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors de la lecture des données des étudiants.")
            return

        try:
            with open(livres_file, "r") as f:
                livres_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Erreur lors de la lecture des données des livres.")
            return

        table = PrettyTable(["ID étudiant", "Nom", "Prénom", "Livre ID", "Date d'emprunt", "Jours ctdwn"])

        for etudiant in redlist_data:
            if "livres_empruntes" in etudiant and etudiant["livres_empruntes"]:
                for livre_id in etudiant["livres_empruntes"]:
                    livre = next((livre for livre in livres_data if livre["id"] == livre_id), None)
                    if livre and "date_emprunt" in livre:
                        for emprunt_info in livre["date_emprunt"]:
                            if emprunt_info["etudiant_id"] == etudiant["id"]:
                                date_emprunt = datetime.strptime(emprunt_info["date_emprunt"], "%Y-%m-%d %H:%M:%S")
                                jours_ctdwn = (datetime.now() - date_emprunt).days
                                if jours_ctdwn > 7:
                                    table.add_row(
                                        [etudiant['id'], etudiant['nom'], etudiant['prenom'], livre_id, date_emprunt,
                                         jours_ctdwn])

        print(table)

    @classmethod
    def verifier_emprunts_en_retard(cls, etudiants_file, livres_file, redlist_file):
        if not cls.user:
            print("Aucun étudiant connecté.")
            return

        with open(etudiants_file, "r") as f:
            etudiants_data = json.load(f)
        with open(livres_file, "r") as f:
            livres_data = json.load(f)

        redlist = []
        logged_in_etudiant = cls.user[0]

        for etudiant in etudiants_data:
            if etudiant.get("id") == logged_in_etudiant.id and "livres_empruntes" in etudiant and etudiant["livres_empruntes"]:
                for livre_id in etudiant["livres_empruntes"]:
                    livre = next((livre for livre in livres_data if livre["id"] == livre_id), None)
                    if livre and "date_emprunt" in livre and livre["date_emprunt"]:
                        for emprunt_info in livre["date_emprunt"]:
                            if emprunt_info["etudiant_id"] == logged_in_etudiant.id:
                                date_emprunt = datetime.strptime(emprunt_info["date_emprunt"], "%Y-%m-%d %H:%M:%S")
                                days_passed = (datetime.now() - date_emprunt).days
                                if days_passed > 7:
                                    redlist.append({
                                        "id": etudiant["id"],
                                        "nom": etudiant["nom"],
                                        "prenom": etudiant["prenom"],
                                        "livres_empruntes": etudiant["livres_empruntes"],
                                        "date_emprunt": emprunt_info["date_emprunt"],
                                        "jours_countdown": days_passed
                                    })
        if redlist:
            try:
                with open(redlist_file, "r") as f:
                    existing_redlist = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_redlist = []

            updated_redlist = existing_redlist + redlist

            with open(redlist_file, "w") as f:
                json.dump(updated_redlist, f, indent=2)
        else:
            print("Aucun retard détecté.")

    @classmethod
    def retirer_redlist(cls, etudiant_id, livre_id, redlist_file):
        try:
            with open(redlist_file, "r") as f:
                redlist_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            redlist_data = []

        updated_redlist = [
            etudiant
            for etudiant in redlist_data
            if etudiant.get("id") != etudiant_id or ("livres_empruntes" in etudiant and livre_id not in etudiant["livres_empruntes"])
        ]

        with open(redlist_file, "w") as f:
            json.dump(updated_redlist, f, indent=2)
    @classmethod
    def notifier_etudiant_in_redlist(cls, redlist_file):
        if not cls.user:
            print("Aucun étudiant connecté.")
            return
        logged_in_etudiant = cls.user[0]
        with open(redlist_file, "r") as f:
            redlist_data = json.load(f)
        for etudiant_in_redlist in redlist_data:
            if etudiant_in_redlist.get("id") == logged_in_etudiant.id:
                print("Attention: Votre emprunt pour certains livres a dépassé la période autorisée. Merci de régulariser votre situation.")
                return

    @classmethod
    def modifier_etudiant(cls, etudiant_id, nv_username=None, nv_nom=None, nv_prenom=None, nv_email=None):
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
                nv_nom = input("Nouveau nom: ")
            elif choix_modification == '2':
                nv_prenom = input("Nouveau prénom: ")
            elif choix_modification == '3':
                nv_email = input("Nouvel email: ")
            elif choix_modification == '4':
                nv_username = input("Nouveau nom d'utilisateur: ")
            elif choix_modification == '5':
                print("Quitter sans modifications.")
                return

            for etudiant in etudiant_data:
                if etudiant['id'] == etudiant_id:
                    if nv_username is not None:
                        etudiant['username'] = nv_username
                    if nv_nom is not None:
                        etudiant['nom'] = nv_nom
                    if nv_prenom is not None:
                        etudiant['prenom'] = nv_prenom
                    if nv_email is not None:
                        etudiant['email'] = nv_email

            with open("listes.json", "w") as f:
                json.dump(etudiant_data, f, indent=2)
                print(f"Étudiant avec ID {etudiant_id} modifié avec succès.")
        else:
            print(f"Aucun étudiant trouvé avec l'ID {etudiant_id}.")


    @classmethod
    def modifier_infos_perso_etudiant(cls, nv_username=None, nv_nom=None, nv_prenom=None, nv_email=None):
        if not cls.user:
            print("Aucun étudiant connecté.")
            return

        logged_in_etudiant = cls.user[0]

        print("Choisissez les modifications pour votre compte:")
        print("1. Changer le nom")
        print("2. Changer le prénom")
        print("3. Changer l'email")
        print("4. Changer le nom d'utilisateur")
        print("5. Quitter sans modifications")

        choix_modification = input("Choix : ")

        if choix_modification in {'1', '2', '3', '4'}:
            if choix_modification == '1':
                nv_nom = input("Nouveau nom: ")
            elif choix_modification == '2':
                nv_prenom = input("Nouveau prénom: ")
            elif choix_modification == '3':
                nv_email = input("Nouvel email: ")
            elif choix_modification == '4':
                nv_username = input("Nouveau nom d'utilisateur: ")

            if nv_username is not None:
                logged_in_etudiant.username = nv_username
            if nv_nom is not None:
                logged_in_etudiant.nom = nv_nom
            if nv_prenom is not None:
                logged_in_etudiant.prenom = nv_prenom
            if nv_email is not None:
                logged_in_etudiant.email = nv_email

            with open("listes.json", "r") as f:
                etudiants_data = json.load(f)

            for etudiant in etudiants_data:
                if etudiant['id'] == logged_in_etudiant.id:
                    etudiant['username'] = logged_in_etudiant.username
                    etudiant['nom'] = logged_in_etudiant.nom
                    etudiant['prenom'] = logged_in_etudiant.prenom
                    etudiant['email'] = logged_in_etudiant.email

            with open("listes.json", "w") as f:
                json.dump(etudiants_data, f, indent=2)
                print("Informations mises à jour avec succès.")
        elif choix_modification == '5':
            print("Quitter sans modifications.")
        else:
            print("Choix invalide.")

    @classmethod
    def menu_etudiant(cls):
        print("**************** Welcome etudiant ****************")

        while True:
            cls.verifier_emprunts_en_retard("listes.json", "livres.json", "redlist.json")
            cls.notifier_etudiant_in_redlist("redlist.json")
            print(class_livre.affichage_livres_etudiant())
            print("Options:")
            print(" A: Emprunter un livre")
            print(" B: Afficher la liste des livres disponibles")
            print(" C: Afficher les livres empruntés")
            print(" D: Retourner un livre")
            print(" E: Modifier le compte")
            print(" X: Retourner")

            choix = input("Saisissez votre choix : ")

            if choix == 'A':
                livre_id = int(input('Choisissez le ID du livre :'))
                cls.emprunter_livre(livre_id, "livres.json", "listes.json", "redlist.json")
                c = int(input("saisir 0 oour retourner au menu : "))
                if c == 0:
                    continue
            elif choix == 'B':
                print(class_livre.affichage_livres_etudiant())
            elif choix == 'C':
                print(cls.affiche_emprunts("livres.json", "listes.json"))
                c = int(input("saisir 0 oour retourner au menu : "))
                if c == 0:
                    continue
            elif choix == 'D':
                livre_id = int(input("Veuillez saisir l'ID du livre : "))
                cls.supprimer_emprunt(livre_id, "listes.json", "livres.json", "redlist.json")
                c = int(input("saisir 0 oour retourner au menu : "))
                if c == 0:
                    continue
            elif choix == 'E':
                cls.modifier_infos_perso_etudiant()
            elif choix == 'X':
                return
            else:
                print("Choix invalide. Veuillez saisir une option valide.")


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
