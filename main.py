from Etudiant import class_etudiant
from Administrateur import Administrateur
from Livre import class_livre
def main_menu():
    print("****************Main Menu****************")
    while True:
        choix = input("A: Admin \n B: Etudiant \n X: retourner \n saisir votre choix : ")
        if choix.upper() == 'A':
            Administrateur.menu_administrateur()
        elif choix.upper() == 'B':
            class_etudiant.menu_etudiant()
        elif choix.upper() == 'X':
            print("goodbye!")
            break
        else:
            print("choix incorrecte")
main_menu()

