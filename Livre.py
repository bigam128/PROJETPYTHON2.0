from prettytable import \
    PrettyTable  ##(pip install prettytable) la commande pour installer PrettyTable pour afficher les livres dans un tableau
import json
from datetime import datetime

class class_livre:
    livres = []
    id = 1
    def __init__(self, id: int, auteur: str, titre: str, editeur: str, ISBN: str, nbr_exemplaire: int, quantite_stock=None,emprunte_par=None, date_emprunt=None):  # constructeur
        self.id = id
        self.auteur = auteur
        self.titre = titre
        self.editeur = editeur
        self.ISBN = ISBN
        self.nbr_exemplaire = nbr_exemplaire
        self.quantite_stock = 0 if quantite_stock is None else quantite_stock
        self.emprunte_par = [] if emprunte_par is None else emprunte_par
        self.date_emprunt = [] if date_emprunt is None else date_emprunt

    @property
    def __str__(self):  # affichage du livre string method
        return f' {self.id} + {self.auteur} + {self.titre}+{self.editeur} + {self.ISBN} + {self.nbr_exemplaire}+{self.emprunte_par}'
        # c = Livre(2,'adam','hh','gh',123, 123)
        # print(c.__str__)
        # affichage -> 2 + adam+hh+....

    def get_table_row(self) -> list:
        return [self.id, self.titre, self.auteur, self.editeur, self.ISBN, self.nbr_exemplaire, self.emprunte_par,self.date_emprunt]

    @classmethod
    def ajouter_un_livre(cls):# demander a l'utilisateur de saisir les informations du livre
        try: #d'abord on commence par ouvrir le fichiers pour appender les nouveaux dans la listes existante
            with open("livres.json", "r") as file:
                livres = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError): #ca n'as pas voulu ouvrir le fichier quand j'ai ecris juste FileNotfounderror
            cls.livres = []
        #max_id = max(livres, key=lambda x: x['id'], default={'id': 0})['id'] # trouver le id max dans la liste key lambda x(element comme livres[...]) fonction pour qui va rendre la valeur id
        #cls.id = int(max_id) + 1 #on ajoute le id depending on the previous id ce qui le MAX!!!
        while True:
            id = int(input('id :'))
            if id == 0:  # STOP!!!!!!!!!!!!
                break
            if any(livre['id'] == id for livre in livres):
                print(f"livre avec id {id}  exists. choisir different id.")
                continue
            auteur = input('auteur : ')
            titre = input('titre :')
            editeur = input('editeur :')
            ISBN = input('ISBN :')
            nbr_exemplaire = 1 # on  le nbr exemplaire a 1 et on ajoute
            livre_instance = {
                'id': id,
                'auteur': auteur,
                'titre': titre,
                'editeur': editeur,
                'ISBN': ISBN,
                'nbr_exemplaire': nbr_exemplaire,
                'quantite_stock': 0,
                'emprunte_par': [],
                'date_emprunt': []
            }
            livres.append(livre_instance)

            for livre in livres:
                livre['quantite_stock'] = int(livre['nbr_exemplaire']) + len(livre.get('emprunte_par', []))
                livre['nbr_exemplaire'] = int(livre['quantite_stock']) - len(livre.get('livres_empruntes', []))

        with open("livres.json", "w") as file:
            json.dump(livres, file, indent=2)
            file.write('\n')
        print('livre ajouter avec succes')
        return livres

    @classmethod
    def ajouter_quantite_stock(cls, livre_id, quantite_stock, livres_file):
        with open(livres_file, "r") as f:
            livres_data = json.load(f)
        livre = next((livre for livre in livres_data if livre['id'] == livre_id), None)

        if livre:
            livre['quantite_stock'] += quantite_stock
            livre['nbr_exemplaire'] += quantite_stock
            with open(livres_file, "w") as f:
                json.dump(livres_data, f, indent=2)
            print(f"Quantité de stock pour le livre avec l'ID {livre_id} ajoutée avec succès.")
        else:
            print(f"Livre avec l'ID {livre_id} non trouvé.")

    @classmethod
    def affichage_livres(cls):
        table = PrettyTable(['id', 'auteur', 'titre', 'editeur', 'ISBN', 'nbr de livres dispo', 'Quantite Stock','emprunter par'])
        try:
            with open("livres.json", "r") as f:
                livres_data = json.load(f)
                for livre_data in livres_data:
                    emprunte_par_id = livre_data.get('emprunte_par')
                    emprunte_par_name = 'Aucun' if emprunte_par_id is None else f"ID: {emprunte_par_id}"
                    date_emprunt = livre_data.get('date_emprunt', 'Non emprunte')
                    table.add_row([livre_data['id'], livre_data['auteur'], livre_data['titre'], livre_data['editeur'],
                                   livre_data['ISBN'], livre_data['nbr_exemplaire'], livre_data['quantite_stock'],emprunte_par_name])
        except FileNotFoundError:
            print("Le fichier n'existe pas.")
        print(table)

    @classmethod
    def affichage_livres_etudiant(cls): # cette fonction va afficher la liste des livres pour l'etudiant il n'as pas a voir le isbn
        table2 = PrettyTable(['id','auteur', 'titre', 'editeur', 'nbr_exemplaire'])
        try:
            with open("livres.json", "r") as f1:
                livre_data = json.load(f1)
                for livree in livre_data:
                    table2.add_row([livree['id'],livree['auteur'],livree['titre'], livree['editeur'], livree['nbr_exemplaire']])
        except FileNotFoundError:
            print("le fichier n'existe pas")
        print(table2)

    @classmethod
    def emprunter_livre(cls, livre_id, etudiant_id, livres_file):
        with open(livres_file, "r") as f:
            livres_data = json.load(f)
            for livres in livres_data:
                livre = next((livre for livre in livres_data if
                          livre['id'] == livre_id and livre['nbr_exemplaire'] > 0), None)
                if livre:
                    # // update : je vais stocker la date dans un array pour avoir la date et le id respectivemment
                    date_emprunt_entree = {
                        'date_emprunt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"), #la date !!! on l'implemente ici car c le bon moment ;)
                        'etudiant_id': etudiant_id,
                        #'livre_id' : livre_id apres je vais la modifier pour mettre c informations dans un nouveau fichier la liste des emprunts
                    }
                    livre['date_emprunt'].append(date_emprunt_entree)
                    livre['emprunte_par'].append(etudiant_id)
                    livre['nbr_exemplaire'] -= 1
                    with open(livres_file, "w") as f:
                        json.dump(livres_data, f, indent=2)
                    return True
                else:
                    print("Erreur Livre non disponible")
                    return False

    @classmethod
    def supp_emprunt(cls, etudiant_id, livre_id, livres_file): #cette methode et plus specifique que celle d'avant qui effacer tous les informations
        with open(livres_file, "r") as f:
            livres_data = json.load(f)
        for livre in livres_data:
            if livre['id'] == livre_id:
                etudiant_index = livre.get("emprunte_par", []).index(etudiant_id) if "emprunte_par" in livre else None
                if etudiant_index is not None:
                    livre["emprunte_par"].pop(etudiant_index)# on efface dans emprunter par le id qu'on veut
                    date_index = None # dans "date_emprunt" on cherche le etudiant id et on l'efface
                    for i, date_info in enumerate(livre.get("date_emprunt", [])):
                        if date_info.get("etudiant_id") == etudiant_id:
                            date_index = i
                            break
                    if date_index is not None:
                        livre["date_emprunt"].pop(date_index)
                    with open(livres_file, "w") as f:
                        json.dump(livres_data, f, indent=2)
                    return True
        print("Livre non trouvé")
        return False

    @classmethod
    def modifier_livre(cls, livre_id, nv_titre=None, nv_auteur=None, nv_exemplaires=None):
        try:
            with open("livres.json", "r") as f:
                livres_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            print("Error loading book data.")
            return

        livre_exist = any(x['id'] == livre_id for x in livres_data)
        if livre_exist:
            print(f"Choisissez les modifications pour le livre avec ID {livre_id}:")
            print("1. Changer le titre")
            print("2. Changer l'auteur")
            print("3. Changer le nombre d'exemplaires")
            print("4. Quitter sans modifications")

            choix_modification = input("Choix : ")

            if choix_modification == '1':
                nv_titre = input("Nouveau titre: ")
            elif choix_modification == '2':
                nv_auteur = input("Nouvel auteur: ")
            elif choix_modification == '3':
                nv_exemplaires = input("Nouveau nombre d'exemplaires: ")
            elif choix_modification == '4':
                print("Quitter sans modifications")
                return

            for livres in livres_data:
                if livres["id"] == livre_id:
                    if nv_titre is not None:
                        livres["titre"] = nv_titre
                    if nv_auteur is not None:
                        livres["auteur"] = nv_auteur
                    if nv_exemplaires is not None:
                        livres["nbr_exemplaire"] = nv_exemplaires

            with open("livres.json", "w") as f:
                json.dump(livres_data, f, indent=2)
                print(f"Livre avec ID {livre_id} modifié avec succès.")
        else:
            print(f"Aucun livre trouvé avec l'ID {livre_id}.")

    @classmethod
    def update_livre_attribute(cls, livre_id, attribute, new_value):
        for livre in cls.livres:
            if livre.id == livre_id:
                setattr(livre, attribute, new_value)

    #@classmethod
    #def supp_emprunt(cls, livre_id, livres_file):  # cette methode pour l'appeler dans supprimer_emprunt class etudiant
        #with open(livres_file, "r") as f:
           # livres_data = json.load(f)
        #for livre in livres_data:
            #if livre['id'] == livre_id:
                #livre['date_emprunt'] = []
               # livre['emprunte_par'] = []
               # with open(livres_file, "w") as f:
                    #json.dump(livres_data, f, indent=2)
                #return True
            #print("Livre non trouvé")
           # return False


#if livre:
    #date_emprunt_entree = {
        ##'date_emprunt': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # la date !!!
        #'etudiant_id': etudiant_id
   # }
    # livre['date_emprunt'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #la date !!! on l'implemente ici car c le bon moment ;)
    #livre['nbr_exemplaire'] -= 1
    #if isinstance(livres['emprunte_par'], list):
        #livres['emprunte_par'] = []
        #livres['emprunte_par'].append(etudiant_id)  # on la rempli par le id etudiant
    #if not isinstance(livres['date_emprunt'], list):
        #livres['date_emprunt'] = []
        #livres['date_emprunt'].append(date_emprunt_entree)#

#@classmethod
    #def livre_existe(cls, id_livre):
        # apres chercher id avec la fonction trouver_livre_id
        #livre_deja_existe = cls.trouver_livre_id()
        # retourne
        #return id_livre in livre_deja_existe

    #@classmethod
    #def trouver_livre_id(cls):
        # with open("livres.txt", "r") as file:
           # content = file.read()
        #livre_deja_existe = []
        #for line in content.split("\n"):
            #if line.startswith("id : "):
                #livre_deja_existe.append(int(line.split(" : ")[1]))

        #return livre_deja_existe





#livres = class_livre.ajouter_un_livre()
#for livre in livres:
    #print(livre.get_table_row())

#trouver l'element du tableau livre
























#tableau_de_livre = [content]
           # for line in content.split('\n'):
                #if line.strip():
                    #key, value = line.split(" : ", 1)
                   # tableau_de_livre.append([key, value])
            #custom_headrs = ["id","auteur", "titre", "editeur", "ISBN", "nbr_exemplaire"]
            #print(tabulate(tableau_de_livre, headers=custom_headrs,tablefmt="grid"))
