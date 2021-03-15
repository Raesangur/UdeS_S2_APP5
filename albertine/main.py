###
###  Gabarit pour l'application de traitement des frequences de mots dans les oeuvres d'auteurs divers
###  Le traitement des arguments a ete inclus:
###     Tous les arguments requis sont presents et accessibles dans args
###     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
###
###  Frederic Mailhot, 26 fevrier 2018
###    Revise 16 avril 2018
###    Revise 7 janvier 2020

###  Parametres utilises, leur fonction et code a generer
###
###  -d   Deja traite dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le repertoire d'auteurs
###       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
###
###  -P   Si utilise, indique au systeme d'utiliser la ponctuation.  Ce qui est considére comme un signe de ponctuation
###       est defini dans la liste PONC
###       Si -P EST utilise, cela indique qu'on désire conserver la ponctuation (chaque signe est alors considere
###       comme un mot.  Par defaut, la ponctuation devrait etre retiree
###
###  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
###
###  -a   Auteur (unique a traiter).  Utile en combinaison avec -g, -G, pour la generation d'un texte aleatoire
###       avec les caracteristiques de l'auteur indique
###
###  -G   Indique qu'on veut generer un texte (voir -a ci-haut), le nombre de mots à generer doit être indique
###
###  -g   Indique qu'on veut generer un texte (voir -a ci-haut), le nom du fichier en sortie est indique
###
###  -F   Indique qu'on desire connaitre le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
###       donné avec le parametre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
###
###  -v   Deja traite dans le gabarit:  mode "verbose",  va imprimer les valeurs données en parametre
###
###
###  Le systeme doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la presence et la valeur
###  des autres parametres, le systeme produira differentes sorties:
###
###  avec -a, -g, -G:  generation d'un texte aleatoire avec les caracteristiques de l'auteur identifie
###  avec -a, -F:  imprimer la frequence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  frequence"
###                la frequence doit être un nombre reel entre 0 et 1, qui represente la probabilite de ce mot
###                pour cet auteur
###  avec -f:  indiquer l'auteur le plus probable du texte identifie par le nom de fichier qui suit -f
###            Format de sortie:  "nom du fichier: auteur"
###  avec ou sans -P:  indique que les calculs doivent etre faits avec ou sans ponctuation
###  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramètres (fait deja partie du gabarit)


import argparse
import collections
import os

### Ajouter ici les signes de ponctuation à retirer
PONC = ["!", '"', "'", ")", "(", ",", ".", ";", ":", "?", "-", "_", "»", "«"]

###  Vous devriez inclure vos classes et méthodes ici, qui seront appellées à partir du main


### Main: lecture des paramètres et appel des méthodes appropriées
###
###       argparse permet de lire les paramètres sur la ligne de commande
###             Certains paramètres sont obligatoires ("required=True")
###             Ces paramètres doivent êtres fournis à python lorsque l'application est exécutée
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    ### Lecture du répertoire des auteurs, obtenir la liste des auteurs
    ### Note:  args.d est obligatoire
    ### auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    ### Enlever les signes de ponctuation (ou non) - Définis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    ### Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Calcul avec les auteurs du repertoire: " + args.d)
        if args.f:
            print("Fichier inconnu a,"
                  " etudier: " + args.f)

        print("Calcul avec des " + str(args.m) + "-grammes")
        if args.F:
            print(str(args.F) + "e mot (ou digramme) le plus frequent sera calcule")

        if args.a:
            print("Auteur etudie: " + args.a)

        if args.P:
            print("Retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

### À partir d'ici, vous devriez inclure les appels à votre code

def print_dictionnairy(dictionairy):
    if args.m == 1:
        # unigramme
        print(dictionairy)

    elif args.m == 2:
        # bigramme
        first_values = list(dictionairy)[:1000]
        print(first_values)


def addInDictionnairy(word, dictionnaire):
    if word in dict:
        # faire +1
        dictionnaire[word] = dictionnaire[word] +1
    else:
        # ajouter le mot
        dictionnaire[word] = 1


def n_gramme_ajout_dict(word1, word2, dictionnaire):
    # unigramme
    if len(word1) > 2 and args.m == 1:
        addInDictionnairy(word1, dictionnaire)

    # bigramme
    if len(word2) < 2 and len(word1) > 2 and args.m == 2:
        # donne la première valeur de word_no_punc_2
        word2 = word1

    elif len(word1) > 2 and len(word2) > 2 and args.m == 2:
        addInDictionnairy(word2 + ' , ' + word1, dictionnaire)
        word2 = word1

    return word1, word2



def readFile(file, autor, dictionnaire):
    # ouvrir fichier
    book = open(rep_aut + '\\' + autor + '\\' + file, 'r', encoding="utf8")

    # read each line
    word_no_punc_2 = ""

    for line in book:
        # autre méthode pour enlever la ponctuation (qui marche pas rip)
        # replace non-alphanumeric char with a space, and then split
        # word_no_punc = (re.sub(PONC, " ", line).split())
        # word_no_punc = word_no_punc.lower()

        for word in line.split():
            # remove punctuation
            word_no_punc = ""

            for char in word:
                if char not in PONC:
                    # enlever les majuscules
                    word_no_punc = (word_no_punc + char).lower()

                if char is "'":
                    # enlève la lettre avant l'apostrophe
                    word_no_punc = ""

                if char is "-":
                    # séparer les deux mots
                    # mettre le premier mot dans la liste

                    # ajoute le mot (s'il y a lieu) en fonction du n
                    word_no_punc, word_no_punc_2 = n_gramme_ajout_dict(word_no_punc, word_no_punc_2, dictionnaire)

                    # remettre une chaine vide pour le mot après le trait d'union
                    word_no_punc = ""

            word_no_punc, word_no_punc_2 = n_gramme_ajout_dict(word_no_punc, word_no_punc_2, dictionnaire)


def dict_pourcentage(dictionary):
    # 1- faire la somme de toutes les valeurs du dictionnaire
    total_sum = sum(dictionary.values())
    print(total_sum)

    # 2- transformer les valeurs du dictionnaire en pourcentage
    for element in dictionary:
        dictionary[element] = dictionary[element] / total_sum


# créer dictionnaire vide
dict = {}


if str(args.a) in ['Balzac']:
    readFile('HonoredeBalzac-Lacomédiehumaine-Volume1.txt', str(args.a), dict)
    readFile('HonoredeBalzac-Lacomédiehumaine-Volume2.txt', str(args.a), dict)
    readFile('HonoredeBalzac-Lacomédiehumaine-Volume3.txt', str(args.a), dict)
    readFile('HonoredeBalzac-Lacomédiehumaine-Volume4.txt', str(args.a), dict)
    readFile('HonoredeBalzac-Lacomédiehumaine-Volume9.txt', str(args.a), dict)

elif str(args.a) in ['Hugo']:
    readFile('Victor Hugo - Les misérables - Tome I.txt', str(args.a), dict)
    readFile('Victor Hugo - Les misérables - Tome II.txt', str(args.a), dict)
    readFile('Victor Hugo - Les misérables - Tome IV.txt', str(args.a), dict)
    readFile('Victor Hugo - Les misérables - Tome V.txt', str(args.a), dict)
    readFile('Victor Hugo - Lhomme qui rit.txt', str(args.a), dict)
    readFile('Victor Hugo - Notre-Dame de Paris.txt', str(args.a), dict)

elif str(args.a) in ['Ségur']:
    readFile('Comtesse de Ségur - François le Bossu.txt', str(args.a), dict)
    readFile('Comtesse de Ségur - Les deux nigauds.txt', str(args.a), dict)
    readFile('Comtesse de Ségur - Les malheurs de Sophie.txt', str(args.a), dict)
    readFile('Comtesse de Ségur - Les mémoires dun ane.txt', str(args.a), dict)
    readFile('Comtesse de Ségur - Un bon petit diable.txt', str(args.a), dict)

elif str(args.a) in ['Verne']:
    readFile('Jules Verne - Autour de la lune.txt', str(args.a), dict)
    readFile('Jules Verne - De la terre a la lune.txt', str(args.a), dict)
    readFile('Jules Verne - Le tour du monde en quatre-vingts jours.txt', str(args.a), dict)
    readFile('Jules Verne - Les enfants du capitaine Grant.txt', str(args.a), dict)
    readFile('Jules Verne - Lile mystérieuse.txt', str(args.a), dict)
    readFile('Jules Verne - Robur-le-conquérant.txt', str(args.a), dict)
    readFile('Jules Verne - Vingt mille lieues sous les mers.txt', str(args.a), dict)
    readFile('Jules Verne - Voyage au centre de la terre.txt', str(args.a), dict)

elif str(args.a) in ['Voltaire']:
    readFile('Voltaire - Candide.txt', str(args.a), dict)
    readFile('Voltaire - Lingénu.txt', str(args.a), dict)
    readFile('Voltaire - Zadig ou la destinée.txt', str(args.a), dict)

elif str(args.a) in ['Zola']:
    readFile('Emile Zola - Germinal.txt', str(args.a), dict)
    readFile('Emile Zola - La bête humaine.txt', str(args.a), dict)
    readFile('Emile Zola - La faute de labbée Mouret.txt', str(args.a), dict)
    readFile('Emile Zola - Lassomoir.txt', str(args.a), dict)
    readFile('Emile Zola - Nana.txt', str(args.a), dict)


# sort dict
list_sorted = sorted(dict.items(), key=lambda x:x[1], reverse=1)
dict = collections.OrderedDict(list_sorted)
#print_dictionnairy(dict)


# Calcul de la proximité d’un autre texte
# 1- transforner le dictionnaire pour que les valeurs soient en pourcentage
dict_pourcentage(dict)
#print_dictionnairy(dict)

# 2- créer le dictionnaire inconnu
dict_inconnu = {}
readFile('Emile Zola - Germinal.txt', str(args.a), dict_inconnu)

# 2- comparer les clés des dictionnaires et faire une moyenne de la ressemblanc des pourcentage
for key in dict:
    if key in dict_inconnu:
        # comparer les pourcentages
    else:
        # jsais pas trop

