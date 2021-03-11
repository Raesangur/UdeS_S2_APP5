#
#  Code pour explorer le premier exercice du laboratoire - S2 APP5i
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
from pythonds.graphs import Graph

###
# Code tiré de la section 7.8 du livre de référence
# À adapter pour l'exercice:
#   - ajouter un arc entre des mots qui ne sont pas de la même longueur mais qui ne diffèrent que par une lettre
#   - permettre des arcs entre des mots qui diffèrent par 2, 3, ... lettres (indiqué sur la ligne de commande)
def buildGraph(wordFile, distance = 1):
    d = {}
    g = Graph()
    wfile = open(wordFile, 'r')
    # create buckets of words that differ by one letter
    for line in wfile:
        word = line[:-1]
        for j in range(len(word)):
            bucket = word[:j] + '_' + word[j + 1:]
            for i in range(len(word)):
                bucket2 = bucket[:i] + '_' + bucket[i+1:]
                if bucket2 in d:
                    d[bucket2].append(word)
                else:
                    d[bucket2] = [word]

    # add vertices and edges for words in the same bucket
    for bucket in d.keys():
        for word1 in d[bucket]:
            for word2 in d[bucket]:
                if word1 != word2:
                    g.addEdge(word1, word2)
                    #print("Linking " + word1 + " & " + word2)
    print(d)
    return g

#  Vous devriez ajouter du code pour accéder au mot de départ (fourni sur la ligne de commande)
#  et ensuite parcourir le graphe jusqu'à une distance D (fournie sur la ligne de commande) du mot d'origine

def printNodes(graph, word, distance, dict = {}):
    currentVertex = graph.vertices[word]
    for vertex in currentVertex.getConnections():
        name = str(vertex.getId())
        if int(distance) != 0:
            dict[name] = name
            printNodes(graph, name, int(distance) - 1, dict)
    return dict

# Main: lecture des paramètres et appel des méthodes appropriées
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='S2-APP5i Labo1:Exercice1.py')
    parser.add_argument('-f', required=True, help='Fichier contenant la liste de mots')
    parser.add_argument('-m', required=True, help='Mot de départ')
    parser.add_argument('-d', required=True, help='Distance du mot de départ')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    args = parser.parse_args()


# Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        print("Mode verbose:")
        print("Fichier de mots utilisé: " + args.f)
        print("Mot de départ: " + args.m)
        print("Distance du mot de départ: " + args.d)


# À partir d'ici, vous devriez inclure les appels requis pour la création du graphe, puis son utilisation
    graph = buildGraph(args.f)
    d = printNodes(graph, args.m, args.d)
    print([key for key in d.keys()])

