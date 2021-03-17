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
import random
import math
import random as rm
from pythonds.graphs import Graph, Vertex
from random import choice


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
    parser.add_argument('-A', action='store_true', help='Analyser tout les auteurs')
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

def print_dictionnairy(dictionairy, number):
    # mettre la variable number à 0 pour faire imprimer toutes les valeurs
    if args.m == 1:
        # unigramme
        if number < 1:
            print(dictionairy)
        else:
            first_values = list(dictionairy)[:number]
            print(first_values)


    elif args.m == 2:
        # bigramme
        first_values = list(dictionairy)[:number]
        print(first_values)

    print("\n\n\n")


def addInDictionnairy(word, dictionnaire):
    if word in dictionnaire:
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
        addInDictionnairy(word2 + ' ' + word1, dictionnaire)
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


def dict_percentage(dictionary, considered_values):
    # 1- calculer la somme de toutes les valeurs du dictionnaire
    # faire la somme des 300 premières valeurs
    total_sum = 0
    iteration = 0
    for element in dictionary:
        total_sum = total_sum + dictionary[element]
        iteration = iteration +1

        if iteration >= considered_values:
            break

    print(total_sum)

    # 2- transformer les valeurs du dictionnaire en pourcentage
    # transformer seulement les 300 premières valeurs
    iteration = 0
    for element in dictionary:
        dictionary[element] = dictionary[element] / total_sum

        iteration = iteration +1
        if iteration >= considered_values+10:
            break


def compare_dictionary(dict_autor, considered_values):
    # comparer les 300 premiers éléments
    somme = 0
    iteration = 0
    for key in dict_autor:
        if key in dict_inconnu:
            # on fait la formule donnée dans le guide
            somme = somme + pow(dict_autor[key] - dict_inconnu[key], 2)
            iteration = iteration + 1

        else:
            somme = somme + pow(dict_autor[key], 2)
            iteration = iteration + 1

        if iteration >= considered_values:
            break

    return math.sqrt(somme)

# def dict_percentage(dictionary):
#     # 1- calculer la somme de toutes les valeurs du dictionnaire
#     total_sum = 0
#     for element in dictionary:
#         total_sum = total_sum + dictionary[element]
#
#     print(total_sum)
#
#     # 2- transformer les valeurs du dictionnaire en pourcentage
#     for element in dictionary:
#         dictionary[element] = dictionary[element] / total_sum
#
#
# def compare_dictionary(dict_autor):
#     somme_pourcentage = 0
#     for key in dict_autor:
#         if key in dict_inconnu:
#             # on divise la plus petite valeur par la plus grande et on fait *100 pour l'avoir en pourcentage
#             if dict_autor[key] <= dict_inconnu[key]:
#                 somme_pourcentage = somme_pourcentage + (dict_autor[key] / dict_inconnu[key]) *100
#
#             else:
#                 somme_pourcentage = somme_pourcentage + (dict_inconnu[key] / dict_autor[key]) *100
#
#     return somme_pourcentage / len(dict_autor)

def create_graph(dictionary):
    graph = Graph()

    for key in dictionary:
        word1, word2 = key.split()
        graph.addEdge(word1, word2, dictionary[key])

    return graph







# créer dictionnaire vide
dict_Balzac = {}
dict_Hugo = {}
dict_Segur = {}
dict_Verne = {}
dict_Voltaire = {}
dict_Zola = {}

print("reading files...")

entries_autor = os.listdir(rep_aut)
for entry in entries_autor:
    if entry == "Balzac" and (args.A or args.a == "Balzac"):
        entries = os.listdir(rep_aut + "\\" + "Balzac")
        for file in entries:
            readFile(file, "Balzac", dict_Balzac)

    if entry == "Hugo" and (args.A or args.a == "Hugo"):
        entries = os.listdir(rep_aut + "\\" + "Hugo")
        for file in entries:
            readFile(file, "Hugo", dict_Hugo)

    if entry == "Ségur" and (args.A or args.a == "Ségur"):
        entries = os.listdir(rep_aut + "\\" + "Ségur")
        for file in entries:
            readFile(file, "Ségur", dict_Segur)

    if entry == "Verne" and (args.A or args.a == "Verne"):
        entries = os.listdir(rep_aut + "\\" + "Verne")
        for file in entries:
            readFile(file, "Verne", dict_Verne)

    if entry == "Voltaire" and (args.A or args.a == "Voltaire"):
        entries = os.listdir(rep_aut + "\\" + "Voltaire")
        for file in entries:
            readFile(file, "Voltaire", dict_Voltaire)

    if entry == "Zola" and (args.A or args.a == "Zola"):
        entries = os.listdir(rep_aut + "\\" + "Zola")
        for file in entries:
            readFile(file, "Zola", dict_Zola)


# sort dict
print("sorting...")
list_sorted_Balzac = sorted(dict_Balzac.items(), key=lambda x:x[1], reverse=1)
list_sorted_Hugo = sorted(dict_Hugo.items(), key=lambda x:x[1], reverse=1)
list_sorted_Segur = sorted(dict_Segur.items(), key=lambda x:x[1], reverse=1)
list_sorted_Verne = sorted(dict_Verne.items(), key=lambda x:x[1], reverse=1)
list_sorted_Voltaire = sorted(dict_Voltaire.items(), key=lambda x:x[1], reverse=1)
list_sorted_Zola = sorted(dict_Zola.items(), key=lambda x:x[1], reverse=1)

dict_Balzac = collections.OrderedDict(list_sorted_Balzac)
dict_Hugo = collections.OrderedDict(list_sorted_Hugo)
dict_Segur = collections.OrderedDict(list_sorted_Segur)
dict_Verne = collections.OrderedDict(list_sorted_Verne)
dict_Voltaire = collections.OrderedDict(list_sorted_Voltaire)
dict_Zola = collections.OrderedDict(list_sorted_Zola)


# MARKOV CHAIN
if (args.m == 2):
    print("Creating Markov chain")

    # 1- créer un graph
    graph = Graph()
    graph = create_graph(dict_Zola)

    # 2- choisir aléatoirement le premier mot
    first_node = random.choice(list(graph.vertices.items()))

if (args.m == 1):
    first_node = random.choice())

















# CALCUL DE LA PROXIMITÉ DE DEUX TEXTES
# 1- lire le texte inconnu
dict_inconnu = {}
readFile(args.f, 'TextesInconnusPourAutoValidation', dict_inconnu)


# sort dict inconnu
list_sorted_inconnu = sorted(dict_inconnu.items(), key=lambda x:x[1], reverse=1)
dict_inconnu = collections.OrderedDict(list_sorted_inconnu)


# 2- transformer les dictionnaires pour que les valeurs soient en pourcentage
considered_values = 300

dict_percentage(dict_Balzac, considered_values)
dict_percentage(dict_Hugo, considered_values)
dict_percentage(dict_Segur, considered_values)
dict_percentage(dict_Verne, considered_values)
dict_percentage(dict_Voltaire, considered_values)
dict_percentage(dict_Zola, considered_values)
dict_percentage(dict_inconnu, 99999999)

print_dictionnairy(dict_Zola, considered_values)
print_dictionnairy(dict_inconnu, 0)

# 3- comparer les clés des dictionnaires et faire une moyenne de la ressemblance des pourcentages
# et imprimer la réponse
if args.A or args.a == "Balzac":
    proximite_Balzac = compare_dictionary(dict_Balzac, considered_values)
    print("Balzac : " + str(proximite_Balzac))

if args.A or args.a == "Hugo":
    proximite_Hugo = compare_dictionary(dict_Hugo, considered_values)
    print("Hugo : " + str(proximite_Hugo))

if args.A or args.a == "Ségur":
    proximite_Segur = compare_dictionary(dict_Segur, considered_values)
    print("Segur : " + str(proximite_Segur))

if args.A or args.a == "Verne":
    proximite_Verne = compare_dictionary(dict_Verne, considered_values)
    print("Verne : " + str(proximite_Verne))

if args.A or args.a == "Voltaire":
    proximite_Voltaire = compare_dictionary(dict_Voltaire, considered_values)
    print("Voltaire : " + str(proximite_Voltaire))

if args.A or args.a == "Zola":
    proximite_Zola = compare_dictionary(dict_Zola, considered_values)
    print("Zola : " + str(proximite_Zola))































