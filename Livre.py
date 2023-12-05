from prettytable import \
    PrettyTable  ##(pip install prettytable) la commande pour installer PrettyTable pour afficher les livres dans un tableau
import json
from datetime import datetime

class class_livre:
    livres = []
    id = 1
    def __init__(self, id: int, auteur: str, titre: str, editeur: str, ISBN: str, nbr_exemplaire: int, emprunte_par=None , date_emprunt= None):  # constructeur
        self.id = id
        self.auteur = auteur
        self.titre = titre
        self.editeur = editeur
        self.ISBN = ISBN
        self.nbr_exemplaire = nbr_exemplaire
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
        max_id = max(livres, key=lambda x: x['id'], default={'id': 0})['id'] # trouver le id max dans la liste key lambda x(element comme livres[...]) fonction pour qui va rendre la valeur id
        cls.id = int(max_id) + 1 #on ajoute le id depending on the previous id ce qui le MAX!!!
        while True:
            auteur = input('auteur : ')
            if auteur == 'stop':  #STOP!!!!!!!!!!!!
                break
            titre = input('titre :')
            editeur = input('editeur :')
            ISBN = input('ISBN :')
            nbr_exemplaire = 1 # on  le nbr exemplaire a 1 et on ajoute
            livre_instance = {
                'id': cls.id,
                'auteur': auteur,
                'titre': titre,
                'editeur': editeur,
                'ISBN': ISBN,
                'nbr_exemplaire': nbr_exemplaire,
                'emprunte_par': [],
                'date_emprunt': []
            }
            livre_exist = next((livre for livre in livres if livre['id'] == cls.id), None)  #trouver si le livre exist pour ajouter le nbr et le id
            if livre_exist:
                livre_exist['nbr_exemplaire'] += 1
            else:
                livres.append(livre_instance) # array!!!!!
                cls.id += 1
        with open("livres.json", "w") as file:
            json.dump(livres, file, indent=2)
            file.write('\n')
        print('livre ajouter avec succes')
        return livres



    @classmethod
    def affichage_livres(cls):
        table = PrettyTable(['id', 'auteur', 'titre', 'editeur', 'ISBN', 'nbr_exemplaire', 'emprunter par','date_emprunt'])
        try:
            with open("livres.json", "r") as f:
                livres_data = json.load(f)
                for livre_data in livres_data:
                    emprunte_par_id = livre_data.get('emprunte_par')
                    emprunte_par_name = 'Aucun' if emprunte_par_id is None else f"ID: {emprunte_par_id}"
                    date_emprunt = livre_data.get('date_emprunt', 'Non emprunte')
                    table.add_row([livre_data['id'], livre_data['auteur'], livre_data['titre'], livre_data['editeur'],
                                   livre_data['ISBN'], livre_data['nbr_exemplaire'], emprunte_par_name, date_emprunt])
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
                        'etudiant_id': etudiant_id
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
    def supp_emprunt(cls, livre_id, livres_file):  # cette methode pour l'appeler dans supprimer_emprunt class etudiant
        with open(livres_file, "r") as f:
            livres_data = json.load(f)
        for livre in livres_data:
            if livre['id'] == livre_id:
                livre['date_emprunt'] = []
                livre['emprunte_par'] = []
                with open(livres_file, "w") as f:
                    json.dump(livres_data, f, indent=2)
                return True
            print("Livre non trouvé")
            return False


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
