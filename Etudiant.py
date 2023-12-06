import json
from prettytable import PrettyTable
from Livre import class_livre
from datetime import datetime

class class_etudiant:
    user = []
    #blacklist_data = []
    #with open("blacklist.json","w") as f:
        #json.dump(blacklist_data, f, indent= 2)
    #print("blacklist.json success")
    def __init__(self, id, nom, prenom, username, email, mdp, livres_empruntes: int = None, suspended=False):
        self.id = id
        self.nom = nom
        self.prenom = prenom
        self.username = username
        self.email = email
        self.mdp = mdp
        self.livres_empruntes = None
        self.suspended = suspended

    def get_usertable_row(self):
        return [self.id, self.nom, self.prenom, self.username, self.email, self.mdp, self.livres_empruntes,self.suspended]

    @classmethod
    def login(cls, username, password, etudiants_file, blackliste_file):  # login pour etudiant
        with open(etudiants_file, "r") as f:
            etudiants_data = json.load(f)
        with open(blackliste_file, "r") as f:
            blackliste_data = json.load(f)
        for etudiant_data in etudiants_data:
            if etudiant_data["username"] == username and etudiant_data["mdp"] == password:
                etudiant_id = etudiant_data["id"]
                blacklisted = any(x["id"] == etudiant_id for x in blackliste_data)
                etudiant = [class_etudiant(
                    etudiant_id,
                    nom=etudiant_data["nom"],
                    prenom=etudiant_data["prenom"],
                    username=etudiant_data["username"],
                    email=etudiant_data["email"],
                    mdp=etudiant_data["mdp"],
                    suspended=blacklisted ##go back to this
                )]
                if blacklisted:
                    print("oups!vous etes bloques")
                    return None
                cls.user = [etudiant]
                return etudiant
        print("mot de passe incorrecte")
        return None

    @classmethod
    def emprunter_livre(cls, livre_id, livres_file, etudiants_file): #mdm
        if not cls.user:
            print("Aucun étudiant connecté.")
            return
        logged_in_etudiant = cls.user[0][0]
        if logged_in_etudiant.livres_empruntes and len(logged_in_etudiant.livres_empruntes) >= 3: #!!!!!!!!!
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
        logged_in_etudiant = cls.user[0][0] #etudiant connecte
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
        logged_in_etudiant = cls.user[0][0] #j'avais ecris que [0] au debut mais ca a donner error
        with open(etudiant_file, "r") as f:
            etudiant_data = json.load(f)
        for idx, etudiant in enumerate(etudiant_data):
            if etudiant["id"] == logged_in_etudiant.id:
                #livres_empruntes = etudiant_data.get("livres_empruntes", [])
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
    def menu_etudiant(cls): #ez
        print("****************Welcome etudiant****************")
        username = input("enter your username : ")
        password = input("enter your password : ")
        logged_in = cls.login(username,password,"listes.json","blacklist.json")
        if logged_in:
            print(f'hello {username}')
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

#class_etudiant.menu_etudiant()
#print(class_etudiant.emprunter_livre(1,"livres.json"))
#print(class_etudiant.affiche_emprunts(1, "listes.json"))







#us = input("enter your username")
#pas = input("entter your password")
#if class_etudiant.login(us, pas):
    #print("login successful")
#else:
    #print("invalid")
