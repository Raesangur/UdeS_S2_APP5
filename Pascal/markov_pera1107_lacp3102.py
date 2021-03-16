#  Gabarit pour l'application de traitement des fréquences de mots dans les oeuvres d'auteurs divers
#  Le traitement des args à été inclus:
#     Tous les args requis sont présents et accessibles dans args
#     Le traitement du mode verbose vous donne un exemple de l'utilisation des args
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
import os
import re
from math import sqrt
from pythonds.graphs import Graph, Vertex
from random import randint
from random import choice

# Ajouter ici les signes de ponctuation à retirer
initialPonc = ['!', '"', '\'', ')', '(', ',', '.', ';', ':', '?', '-', '_', '«', '»', '\n', '\t', ' ', '\xa0']
# initialPonc = ['!', '"', '\'', ')', '(', ',', '.', ';', ':', '?', '-', '_', '»', '«']
PONC = '|'.join(['\\' + x for x in initialPonc])


def ParseArgs():
    parser = argparse.ArgumentParser(prog='markov_cip1_cip2.py')
    parser.add_argument('-d', required=True, help='Repertoire contenant les sous-repertoires des auteurs')
    parser.add_argument('-a', help='Auteur a traiter')
    parser.add_argument('-A', action='store_true', help='Traiter tous les auteurs')
    parser.add_argument('-f', help='Fichier inconnu a comparer')
    parser.add_argument('-m', required=True, type=int, choices=range(1, 3),
                        help='Mode (1, 2 ou 3) - unigrammes, bigrammes ou trigrammes')
    parser.add_argument('-F', type=int, help='Indication du rang (en frequence) du mot (ou bigramme) a imprimer')
    parser.add_argument('-G', type=int, help='Taille du texte a generer')
    parser.add_argument('-g', help='Nom de base du fichier de texte a generer')
    parser.add_argument('-v', action='store_true', help='Mode verbose')
    parser.add_argument('-P', action='store_true', help='Retirer la ponctuation')
    return parser.parse_args()


def PrintVerbose(args, rep_aut, authors):
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
        print("Ne pas retirer les signes de ponctuation suivants: {0}".format(" ".join(str(i) for i in PONC)))

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


def GetPath(path: str) -> str:
    """
        Get normalized path that os.read() can open and read
    :param path: Path to normalize
    :return:     Normalized path
    """
    if os.path.isabs(path):
        rep = path
    else:
        rep = os.path.join(os.getcwd(), path)
    return os.path.normpath(rep)


def AddToDict(dictionary: {str: int},
              newWord: str, count: int = 1):
    """
        Add a string to an existing dictionary
    :param dictionary: Existing dictionary into which the new element should be inserted
    :param newWord:    Element to insert
    :param count:      Value to add to dictionary at key newWord
    """
    if newWord in dictionary:
        dictionary[newWord] += count
    else:
        dictionary[newWord] = count


def SortDict(dictionnary: {str: int}) -> list:
    """
        Sorts a dictionnary by values
    :param dictionnary: The dictionnary to sort
    :return:            A list containing sorted tuples of (key, value)
    """
    return sorted(dictionnary.items(), key=lambda x: x[1], reverse=True)


def ReadBook(bookpath: str,
             book_content: {str, int},
             remove_ponc: bool,
             ngrams: int):
    """
        Read a `.txt`-extention book from path, and insert all it's n-grams into an existing dictionary.
        This function parses each word individually, line by line, removing punctuation (see `PONC`), words with less
        than 3 letters, and turning all letters to lowercase.
    :note  If the `-P` argument is used, punctuation is kept
    :param bookpath:     Path of the book to read (with .txt extension)
    :param book_content: Existing dictionary into which new words will be inserted
    :param remove_ponc:  Remove punctuation
    :param ngrams:       Use unigrams or bigrams of words
    """
    if bookpath[-4:] != ".txt":
        return

    file = open(bookpath, 'r', encoding="utf8")
    for line in file.readlines():
        if remove_ponc:
            words = [x.lower() for x in re.split(PONC, line) if x != '' and len(x) > 2]
        else:
            words = [x.lower() for x in line.split() if len(x) > 2]

        if ngrams == 1:
            for word in words:
                AddToDict(book_content, word)

        elif ngrams == 2:
            for word1, word2 in zip(words, words[1:]):
                newWord = word1 + ' ' + word2
                AddToDict(book_content, newWord)

    file.close()


def ReadBooks(path: str,
              books: [str],
              remove_ponc: bool,
              ngrams: int) -> {str: int}:
    """
        Read all the specified books (.txt extension) in the specified path
    :param path:         Path to the books
    :param books:        List with the name of the book files
    :param remove_ponc:  Remove punctuation
    :param ngrams:       Use unigrams or bigrams of words
    :return: Dictionary containing all the words and their occurence count
    """
    books_content = {}
    for currentBook in books:
        rep_book = os.path.normpath(path + '\\' + currentBook)
        ReadBook(rep_book, books_content, remove_ponc, ngrams)

    return books_content


def ReadAuthor(path: str,
               author: str,
               remove_ponc: bool,
               ngrams: int) -> [(str, int)]:
    """
        Read all the books from an author
    :param path:         Path of the folder containing the author's folder
    :param author:       Name of the author
    :param remove_ponc:  Remove punctuation
    :param ngrams:       Use unigrams or bigrams of words
    :return: Sorted list of all the author's words and their occurence count
    """
    rep_books = os.path.normpath(path + "\\" + author)
    books = os.listdir(rep_books)

    grammes = ReadBooks(rep_books, books, remove_ponc, ngrams)
    grammes = SortDict(grammes)
    return grammes


def BuildPercentList_CalculateTotal(words: [(str, int)]) -> int:
    """
        Calculate total occurence of all provided words
    :param words: List of words to sum up
    :return:      Total occurences
    """
    return sum([x[1] for x in words])


def BuildPercentList_Generator(words: [(str, int)],
                               totalWords: int) -> (str, int):
    """
        Generator function, yielding tuples containing a word, and their chance of occuring according to the total
        number of words.
    :param words:      List of words
    :param totalWords: Total number of words
    :returns:          Yields a word with its percentage chance of occuring
    """
    for word in words:
        yield word[0], word[1] / totalWords * 100


def BuildPercentList(authorWords: {str: [(str, int)]},
                     maxWords: int = 300) -> {str: [(str, int)]}:
    """
        Takes all the authors and calculate the percentage chance that a specific word appears in their works.
    :param authorWords: Dictionary, using the author's name as key, and containing a list of words with their occurence
                        count.
    :param maxWords:    Maximum number of words to calculate percentage with.
                        If set to -1, use all words
    :return:            Dictionary, using the author's name as key, and containing a list of words with their percentage
                        chance of occuring.
    """
    percentWords: {str: [(str, int)]} = {}

    for author in authorWords.items():
        if maxWords == -1:
            maxWords = len(author[1])

        percentWords[author[0]] = []
        totalWords = BuildPercentList_CalculateTotal(author[1][:maxWords])
        for word in BuildPercentList_Generator(author[1][:maxWords], totalWords):
            percentWords[author[0]].append(word)

    return percentWords


def CalculateProximity(authorPercent: [(str, int)],
                       otherPercent: [(str, int)]) -> float:
    r"""
        Calculate the proximity between an author's text and another work's text
        This function uses the following formula:

        .. math::
            \sqrt(\sum_{i=0}^{N}(a_i - t_i)^{2})

    :param authorPercent: Percentage occurence of each ngrams
    :param otherPercent:  Percentage occurence of each ngrams
    :return:              Proximity factor between two texts
    """
    val = 0.0
    authorPercent = dict(authorPercent)
    otherPercent = dict(otherPercent)
    for a, t in [(authorWord[1], otherPercent[authorWord[0]]) for authorWord in authorPercent.items() if authorWord[0] in otherPercent]:
        val += (a - t)**2

    return sqrt(val)


def FindProbableAuthor(path_text: str,
                       authorWords: {str: [(str, int)]},
                       remove_ponc: bool,
                       ngrams: int) -> (str, float):
    """
        Find the most probable author of a .txt document, comparing the ngrams of both
    :param path_text:   Complete path to a .txt file
    :param authorWords: Dictionary using an author's name as key, and using a sorted list of word occurence as value.
    :param remove_ponc: Remove punctuation
    :param ngrams:      Use unigrams or bigrams of words
    :return:            Tuple of an author and their probability factor of being the author of the unknown text
    """

    percentList: {str: [(str, int)]} = BuildPercentList(authorWords)
    for author in percentList.items():
        print(author[0] + ": " + str([x[0] + ": {:0.1f}%".format(x[1]) for x in author[1][:5]]))

    otherbook = {}
    ReadBook(GetPath(path_text), otherbook, remove_ponc, ngrams)
    otherbook = SortDict(otherbook)
    totalWords = BuildPercentList_CalculateTotal(otherbook)
    otherPercent: [(str, int)] = []
    for word in BuildPercentList_Generator(otherbook, totalWords):
        otherPercent.append(word)

    print("Other book: " + str([x[0] + ": {:0.1f}%".format(x[1]) for x in otherPercent[:5]]))

    proximityList = [(a[0], CalculateProximity(a[1], otherPercent)) for a in percentList.items()]
    # print(proximityList)

    guess = max(proximityList, key=lambda x: x[1])
    return guess


def CreateSubDict(authorWords: {str: [(str, int)]},
                  author: str) -> {str: [(str, int)]}:
    var = authorWords[author]
    return {author: var}


def CombineDict(authorWords: {str: [(str, int)]}) -> {str: int}:
    dictionary = {}
    for subdict in authorWords.items():
        for word in subdict[1]:
            AddToDict(dictionary, word[0], word[1])

    return dictionary


def FindnthWord(n: int,
                authorWords: {str: [(str, int)]}) -> (str, int):
    return authorWords.items()[1][n]


def CreateGraph(wordList: [(str, int)]) -> Graph:
    g = Graph()
    for bigram in wordList:
        word1, word2 = tuple(bigram[0].split())
        g.addEdge(word1, word2, bigram[1])

    return g


def PrintGraph(g: Graph):
    for vertex in g.vertices.values():
        print(vertex.getId())
        for edge in vertex.getConnections():
            print("\t" + edge.getId() + ":\t" + str(vertex.getWeight(edge)))


def GetRandomVertex(g: Graph) -> str:
    rand = randint(0, len(g.getVertices()))
    return g.getVertices()[rand]


def GetNextVertex(g: Graph,
                  v: str) -> str:
    v = g.vertices[v]
    total = sum([x[1] for x in v.connectedTo.items()])
    if total == 0:
        return GetRandomVertex(g)

    rand = randint(0, total)
    for edge in v.getConnections():
        rand -= v.getWeight(edge)
        if rand <= 0:
            return edge.getId()


def GenerateText(wordList: [(str, int)],
                 numberWords: int,
                 ngrams: int) -> str:
    text = ""
    g = CreateGraph(wordList)

    vertex = GetRandomVertex(g)
    text += vertex

    for wordIndex in range(0, numberWords):
        vertex = GetNextVertex(g, vertex)
        text += " " + vertex

    return text


# Main: lecture des paramètres et appel des méthodes appropriées
#       argparse permet de lire les paramètres sur la ligne de commande
def main():
    args = ParseArgs()

    # Lecture du répertoire des auteurs, obtenir la liste des auteurs
    # Note:  args.d est obligatoire
    # auteurs devrait comprendre la liste des répertoires d'auteurs, peu importe le système d'exploitation
    rep_aut = GetPath(args.d)
    authors = os.listdir(rep_aut)

    # Si mode verbose, refléter les valeurs des paramètres passés sur la ligne de commande
    if args.v:
        PrintVerbose(args, rep_aut, authors)

    # À partir d'ici, vous devriez inclure les appels à votre code

    # Check inputs:
    if args.a and args.A:
        print("Args -a {0} and -A have both been provided, -a input will be ignored".format(args.a))
        args.a = None

    # List all the words of the different authors
    authorWords: {str: [(str, int)]} = {}
    for a in authors:
        authorWords[a] = ReadAuthor(rep_aut, a, not args.P, args.m)
        # print(a + ": " + str(authorWords[a][:3]))

    # Find the nth word for a specified author
    if args.F:
        if args.A:
            n = FindnthWord(args.F, CombineDict(authorWords))
            print(n)

        elif args.a:
            n = FindnthWord(args.F, CreateSubDict(authorWords, args.a))
            print(n)

        else:
            print("Author wasn't specified, try again")

    # Find the most probable author for a certain text
    if args.f:
        if args.A:
            guess = FindProbableAuthor(args.f, authorWords, not args.P, args.m)
            print(guess)

        elif args.a:
            guess = FindProbableAuthor(args.f, CreateSubDict(authorWords, args.a), not args.P, args.m)
            print(guess)

        else:
            print("Author wasn't specified, try again")

    if args.G:
        text = ""
        if args.m == 2:
            if args.A:
                text = GenerateText([(x[0], x[1]) for x in list(CombineDict(authorWords).items())], args.G, args.m)
            elif args.a:
                text = GenerateText(authorWords[str(args.a)][:], args.G, args.m)

        print(text)


if __name__ == "__main__":
    main()
