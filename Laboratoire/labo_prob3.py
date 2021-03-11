import argparse
import glob
import sys
import os

class myClass:
    def __init__(self, a = None, b = None):
        self.a, self.b = a, b

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.a == other.a and self.b == other.b

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.a, self.b))

def main():
    parser = argparse.ArgumentParser(prog="BonMatin3.py")
    parser.add_argument("-f1", required=True, help="Premier fichier à comparer")
    parser.add_argument("-f2", required=True, help="Deuxième fichier à comparer")
    args = parser.parse_args()


    file1 = open(args.f1, "r")
    file2 = open(args.f2, "r")
    d1 = {}
    d2 = {}

    for line in file1:
        word = line.split()
        d1[myClass(word[0], word[1])] = word

    for line in file2:
        word = line.split()
        d2[myClass(word[0], word[1])] = word

    print("Unique pairs from file2: \n" + str('\n'.join([str((x.a, x.b)) for x in d2 if x not in d1])))

if __name__ == "__main__":
    main()