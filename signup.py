import hashlib

from prettytable import PrettyTable


class Signup:
    def __init__(self, nom, prenom, email, mdp, confirmer_mdp):
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.mdp = mdp
        self.confirmer_mdp = confirmer_mdp

    @classmethod
    def ajouter_user(cls):
        nom = input('Saisir nom : ')
        prenom = input('Saisir prenom : ')
        email = input('Saisir email sous forme (exemple@gmail.com): ')
        mdp = input("Saisir le mot de passe : ")
        confirmer_mdp = input('Confirmer le mot de passe : ')
        if confirmer_mdp == mdp:
            # Hasher le mot de passe avec MD5 
            encrypted = mdp.encode()
            hash_mdp = hashlib.md5(encrypted).hexdigest()
            return cls(nom, prenom, email, hash_mdp, confirmer_mdp)
        else:
            print('Veuillez saisir le même mot de passe.')
            return None

    def afficher_user(self):
        table = PrettyTable(['nom', 'prenom', 'email', 'mdp'])
        table.add_row([self.nom, self.prenom, self.email, self.mdp])
        print(table)


# Créez une instance de Signup en appelant la méthode de classe ajouter_user
user_instance = Signup.ajouter_user()
 # Affichez les informations de l'utilisateur en appelant la méthode d'instance afficher_user
user_instance.afficher_user()
