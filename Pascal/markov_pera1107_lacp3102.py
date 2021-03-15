#
#  Gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers
#  Le traitement des arguments à été inclus:
#     Tous les arguments requis sont présents et accessibles dans args
#     Le traitement du mode verbose vous donne un exemple de l'utilisation des arguments
#
#  Frederic Mailhot, 26 février 2018
#    Revisé 16 avril 2018
#    Revisé 7 janvier 2020

#  Paramêtres utilisés, leur fonction et code a générer
#
#  -d   Deja traité dans le gabarit:  la variable rep_auth contiendra le chemin complet vers le répertoire d'auteurs
#       La liste d'auteurs est extraite de ce repertoire, et est comprise dans la variable authors
#
#  -P   Si utilisé, indique au systeme d'utiliser la ponctuation. Ce qui est considére comme un signe de ponctuation
#       est défini dans la liste PONC
#       Si -P est utilisé, cela indique qu'on désire conserver la ponctuation (chaque signe est alors considéré
#       comme un mot.  Par défaut, la ponctuation devrait être retirée
#
#  -m   mode d'analyse:  -m 1 indique de faire les calculs avec des unigrammes, -m 2 avec des bigrammes.
#
#  -a   Auteur (unique à traiter).  Utile en combinaison avec -g, -G, pour la génération d'un texte aléatoire
#       avec les caractéristiques de l'auteur indiqué
#
#  -G   Indique qu'on veut générer un texte (voir -a ci-haut), le nombre de mots à genérer doit être indiqué
#
#  -g   Indique qu'on veut générer un texte (voir -a ci-haut), le nom du fichier en sortie est indiqué
#
#  -F   Indique qu'on désire connaître le rang d'un certain mot pour un certain auteur.  L'auteur doit etre
#       donné avec le paramêtre -a, et un mot doit suivre -F:   par exemple:   -a Verne -F Cyrus
#
#  -v   Déjà traité dans le gabarit:  mode "verbose",  va imprimer les valeurs données en paramêtre
#
#
#  Le système doit toujours traiter l'ensemble des oeuvres de l'ensemble des auteurs.  Selon la présence et la valeur
#  des autres paramêtres, le système produira differentes sorties:
#
#  avec -a, -g, -G:  génération d'un texte aléatoire avec les caractéristiques de l'auteur identifié
#  avec -a, -F:  imprimer la fréquence d'un mot d'un certain auteur.  Format de sortie:  "auteur:  mot  fréquence"
#                la fréquence doit être un nombre réel entre 0 et 1, qui représente la probabilité de ce mot
#                pour cet auteur
#  avec -f:  indiquer l'auteur le plus probable du texte identifié par le nom de fichier qui suit -f
#            Format de sortie:  "nom du fichier: auteur"
#  avec ou sans -P:  indique que les calculs doivent être faits avec ou sans ponctuation
#  avec -v:  mode verbose, imprimera l'ensemble des valeurs des paramètres (fait déjà partie du gabarit)


import argparse
import glob
import sys
import os
import re
from collections import OrderedDict
from pathlib import Path
from random import randint
from random import choice

# Ajouter ici les signes de ponctuation à retirer
initialPonc = ['!', '"', '\'', ')', '(', ',', '.', ';', ':', '?', '-', '_', '«', '»', '\n', '\t', ' ']
# initialPonc = ['!', '"', '\'', ')', '(', ',', '.', ';', ':', '?', '-', '_', '»', '«']
PONC = '|'.join(['\\' + x for x in initialPonc])


def AddToDict(dictionary, newWord):
    """
        Add a string to an existing dictionary
    :param dictionary: Existing dictionary into which the new element should be inserted
    :param newWord:    Element to insert
    """

    # Adding a string to an existing dictionnary
    if newWord in dictionary:
        dictionary[newWord] += 1
    else:
        dictionary[newWord] = 1


def ReadBook(bookpath, book_content):
    """
    Read a `.txt`-extention book from path, and insert all it's n-grams into an existing dictionary.
    This function parses each word individually, line by line, removing punctuation (see `PONC`), words with less than
    3 letters, and turning all letters to lowercase.
    :note  If the `-P` argument is used, punctuation is kept
    :param bookpath:     Path of the book to read (with .txt extension)
    :param book_content: Existing dictionary into which new words will be inserted
    """
    if bookpath[-4:] != ".txt":
        return

    file = open(bookpath, 'r', encoding="utf8")

    for line in file.readlines():
        if not remove_ponc:
            words = [x.lower() for x in re.split(PONC, line) if x != '' and len(x) > 2]
        else:
            words = [x.lower() for x in line.split() if len(x) > 2]

        if args.m == 1:
            for word in words:
                AddToDict(book_content, word)

        elif args.m == 2:
            for word1, word2 in zip(words, words[1:]):
                newWord = word1 + ' ' + word2
                AddToDict(book_content, newWord)


def ReadBooks(path, books):
    """
    Read all the specified books (.txt extension) in the specified path
    :param path:  Path to the books
    :param books: List with the name of the book files
    :return: Dictionary containing all the words and their occurence count
    """
    books_content = {}
    for currentBook in books:
        rep_book = os.path.normpath(path + '\\' + currentBook)
        ReadBook(rep_book, books_content)

    return books_content


def ReadAuthor(author):
    """
    Read all the books from an author
    :param author: Name of the author
    :return: Sorted list of all the author's words and their occurence count
    """
    rep_books = os.path.normpath(rep_aut + "\\" + author)
    books = os.listdir(rep_books)

    grammes = ReadBooks(rep_books, books)
    grammes = sorted(grammes.items(), key=lambda x: x[1], reverse=True)
    return grammes



# Main: lecture des paramètres et appel des méthodes appropriées
#
#       argparse permet de lire les paramètres sur
# # def CalcPercent(dictionary):
# #    sumWord =la ligne de commande
#             Certains paramàtres sont obligatoires ("required=True")
#             Ces paramètres doivent êtres fournis à python lorsque l'application est exécutée
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 4),
                        help='Mode (1, 2 ou 3) - unigrammes, bigrammes ou trigrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    args = parser.parse_args()

    # Lecture du répertoire des auteurs, obtenir la liste des auteurs
    # Note:  args.d est obligatoire
    # auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    cwd = os.getcwd()
    if os.path.isabs(args.d):
        rep_aut = args.d
    else:
        rep_aut = os.path.join(cwd, args.d)

    rep_aut = os.path.normpath(rep_aut)
    authors = os.listdir(rep_aut)

    # Enlever les signes de ponctuation (ou non) - Définis dans la liste PONC
    if args.P:
        remove_ponc = True
    else:
        remove_ponc = False

    # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
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

        if args.M:
            print("Retirer les majuscules et considérer tous les mots comme minuscules")

        if args.G:
            print("Generation d'un texte de " + str(args.G) + " mots")

        if args.g:
            print("Nom de base du fichier de texte genere: " + args.g)

        print("Repertoire des auteurs: " + rep_aut)
        print("Liste des auteurs: ")
        for a in authors:
            aut = a.split("/")
            print("    " + aut[-1])

    # À partir d'ici, vous devriez inclure les appels à votre code
    authorWords = {}
    for a in authors:
        authorWords[a] = ReadAuthor(a)
        print(a + ": " + str(authorWords[a][:3]))

    #if args.f and args.a:
