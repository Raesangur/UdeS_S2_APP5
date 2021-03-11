#
#  Code pour explorer le deuxième exercice du laboratoire - S2 APP5i
#  Le traitement des arguments a été inclus:
#     Tous les arguments requis sont présents et accessibles dans args
#     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
#
#  Frédéric Mailhot, 28 février 2018
#


import math
import argparse
import glob
import sys
import os

filename = "C:\\Users\\Pascal5333\\Desktop\\tree.py"
exec(compile(open(filename, "rb").read(), filename, "exec"), globals(), locals())

#  Vous devriez inclure vos classes et méthodes ici, qui seront appellées à partir du main
#  Commencer avec le code disponible à la section 6.17 du livre.
#  Vous y trouverez le nécessaire pour utiliser un arbre AVL
#   Vous devrez écrire la méthode rotateRight (qui est analogue à la méthode rotateLeft fournie



# Main: lecture des paramètres et appel des méthodes appropriées
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='S2-APP5i Labo1:Exercice1.py')
    parser.add_argument('-f', required=True, help='Fichier contenant les nombres à ordonner')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    args = parser.parse_args()

# Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v :
        print("Mode verbose:")
        print("Fichier de nombres: " + args.f)



# À partir d'ici, vous devriez inclure les appels à votre code
    tree = AVL_Tree()
    file = open(args.f, "r")
    alph = [char for char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    count = 0
    for line in file:
        count = (count + 1) % len(alph)
        num = int(line)
        tree.put(num, alph[count])

    list = [n[0] for n in tree]
    print(list)
    sys.exit(not all(list[i] <= list[i + 1] for i in range(len(list) - 1)))