
from Uttilisateurs import class_utilisateurs

def main_menu():
    print("****************Main Menu****************")
    print(class_utilisateurs.login("listes.json","blacklist.json"))
main_menu()

