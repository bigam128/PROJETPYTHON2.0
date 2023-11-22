from Etudiant import class_etudiant
from Administrateur import  Administrateur
from Livre import class_livre
i = input('chois A ou E')
if i == 'A':
    Administrateur.menu_administrateur()
elif i == 'E':
    class_etudiant.menu_etudiant()
