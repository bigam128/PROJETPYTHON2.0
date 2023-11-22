from prettytable import \
    PrettyTable  ##(pip install prettytable) la commande pour installer PrettyTable pour afficher les livres dans un tableau

from tabulate import tabulate
import json
class class_livre:
    livre = []
    id = 1
    def __init__(self, id: int, auteur: str, titre: str, editeur: str, ISBN: str, nbr_exemplaire: int, emprunte_par: int = None):  # constructeur
        self.id = id
        self.auteur = auteur
        self.titre = titre
        self.editeur = editeur
        self.ISBN = ISBN
        self.nbr_exemplaire = nbr_exemplaire
        self.emprunte_par = emprunte_par

    @property
    def __str__(self):  # affichage du livre string method
        return f' {self.id} + {self.auteur} + {self.titre}+{self.editeur} + {self.ISBN} + {self.nbr_exemplaire}+{self.emprunte_par}'
        # c = Livre(2,'adam','hh','gh',123, 123)
        # print(c.__str__)
        # affichage -> 2 + adam+hh+....

    def get_table_row(self) -> list:
        return [self.id, self.titre, self.auteur, self.editeur, self.ISBN, self.nbr_exemplaire, self.emprunte_par]
    @classmethod
    def get_livres_file(cls):
        with open("livres.json", "r") as f2:
            cls.livre = json.load(f2)
        return cls.livre

    @classmethod
    def ajouter_un_livre(cls):# demander a l'utilisateur de saisir les informations du livre
        #global livre_instance
        livres = []
        #table = PrettyTable(['id', 'auteur', 'titre', 'editeur', 'ISBN', 'nbr_exemplaire'])
        while True:
            auteur = input('auteur : ')
            if auteur == 'stop':  #STOP!!!!!!!!!!!!
                break
            titre = input('titre :')
            editeur = input('editeur :')
            ISBN = input('ISBN :')
            nbr_exemplaire = 1 # on  le nbr exemplaire a 0 et on ajoute
            livre_instance = cls(id=cls.id, auteur=auteur, titre=titre, editeur=editeur, ISBN=ISBN, nbr_exemplaire=nbr_exemplaire)
            livre_exist = next((livre for livre in livres if livre.titre == titre and livre.auteur == auteur and livre.editeur == editeur and livre.ISBN == ISBN), None) #on verifie si les informations se repete pour additioner le nbr exemplaire
            if livre_exist:
                livre_exist.nbr_exemplaire += 1
            else:
                cls.id += 1 # on incremente le id juste apres ajouter le livre
                livres.append(livre_instance)  # array!!!!!
            #table.add_row(livre_instance.get_table_row())
        with open("livres.json", "a") as file:
            json.dump([livre_instance.__dict__ for livre_instance in livres], file, indent=2)
            file.write('\n')
        print('livre ajouter avec succes')
            #for livre in livres:
                #print(livre.get_table_row())
                #a = livre.get_table_row()[4]
                #print(a)
        return livres

    @classmethod
    def affichage_livres(cls):# affichage du tableau en mode pretty table
        table = PrettyTable(['id', 'auteur', 'titre', 'editeur', 'ISBN', 'nbr_exemplaire','emprunter par'])
        try:
            with open("livres.json", "r") as f:
                livres_data = json.load(f)
                for livre_data in livres_data:
                    table.add_row([livre_data['id'], livre_data['auteur'], livre_data['titre'], livre_data['editeur'], livre_data['ISBN'], livre_data['nbr_exemplaire'],livre_data.get('emprunte_par', 'Aucun')])
        except FileNotFoundError:
            print("the file does not exist")
        print(table)
    @classmethod
    def affichage_livres_etudiant(cls): # cette fonction va afficher la liste des livres pour l'etudiant il n'as pas a voir le id ni le isbn
        table2 = PrettyTable(['id','auteur', 'titre', 'editeur', 'nbr_exemplaire'])
        try:
            with open("livres.json", "r") as f1:
                livre_data = json.load(f1)
                for livree in livre_data:
                    table2.add_row([livree['id'],livree['auteur'],livree['titre'], livree['editeur'], livree['nbr_exemplaire']])
        except FileNotFoundError:
            print("le fichier n'existe pas")
        print(table2)

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
