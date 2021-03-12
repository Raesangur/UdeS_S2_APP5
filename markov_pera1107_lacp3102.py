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


import math
import argparse
import glob
import sys
import os
import re
from pathlib import Path
from random import randint
from random import choice

# Ajouter ici les signes de ponctuation à retirer
#PONC1 = "\\!|\\'|\\)|\\(|\\,| |\\.|; |: |\\?|\\-|_|\n"
PONC = '|'.join(['\\' + x for x in ['!', "'", ')', '(', ',', ' ', '.', ';', ':', '?', '-', '_', '«', '»', '\n', '\t']])


#  Vous devriez inclure vos classes et méthodes ici, qui seront appellées à partir du main


# Main: lecture des paramètres et appel des méthodes appropriées
#
#       argparse permet de lire les paramètres sur la ligne de commande
#             Certains paramàtres sont obligatoires ("required=True")
#             Ces paramètres doivent êtres fournis à python lorsque l'application est exécutée
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 2),
                        help='Mode (1 ou 2) - unigrammes ou digrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    parser.add_argument('-M', action='store_true', help='Retirer les majuscules')
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
    rep_books = os.path.normpath(rep_aut + "\\" + args.a)
    books = os.listdir(rep_books)
    print(books)

    # book_content = []
    # rep_book = os.path.normpath(rep_books + '\\' + books[1])
    # file = open(rep_book, 'r', encoding="utf8")
    # for line in file.readlines():
    #     if remove_ponc:
    #         words = [x for x in re.split(PONC, line) if x != '']
    #     else:
    #         words = line.split()
    #
    #     book_content.extend(words)
    #
    # print(book_content)

    book_content = {}
    rep_book = os.path.normpath(rep_books + '\\' + books[1])
    file = open(rep_book, 'r', encoding="utf8")
    for line in file.readlines():
        if remove_ponc:
            words = [x.lower() if args.M else x for x in re.split(PONC, line) if x != '']
        else:
            words = line.split()

        if args.m == 1:
            for word in words:
                if len(word) <= 2:
                    continue

                if word in book_content:
                    book_content[word] += 1
                else:
                    book_content[word] = 1
        elif args.m == 2:
            for word1, word2 in zip(words):
                newWord = word1 + ' ' + word2

                if newWord in book_content:
                    book_content[newWord] += 1
                else:
                    book_content[newWord] = 1

    print(book_content)

    bestword = ("BonMatin", 1)
    for word in book_content.keys():
        if book_content[word] > bestword[1]:
            bestword = word, book_content[word]

    print(bestword)