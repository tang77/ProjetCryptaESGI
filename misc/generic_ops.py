#! /usr/bin/env python
#coding: utf-8

#IMPORTS
import argparse
import copy
import re

def suppr_bad_chars(ligne):
    """ Tableau des accents """
    accents = {
        'a': ['à', 'ã', 'á', 'â'],
        'e': ['é', 'è', 'ê', 'ë'],
        'i': ['î', 'ï'],
        'u': ['ù', 'ü', 'û'],
        'o': ['ô', 'ö']
    }

    """ Iteration pour supprimer les accents """
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            ligne = ligne.replace(accented_char, char)

    """ Suppression des chars non alpha """
    ligne = re.sub('[^A-Za-z]+', '', ligne)

    return ligne


def get_n_word(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def count_n_gram(text, dico, n):
    for n_gram in get_n_word(text, n):
        if len(n_gram) >= n:
            if n_gram in dico:
                dico[n_gram] += 1
            else:
                dico[n_gram] = 1

def parserMenu():
    """Generate a parser for our stats prog"""
    parser = argparse.ArgumentParser(description='Process some parameters for our stats prog decipher.')
    parser.add_argument('--referentialtext', help='Referential text input for analysis', type=argparse.FileType('r'))
    parser.add_argument('--deciphertext', help='Decipher text input', type=argparse.FileType('r'))

    args = parser.parse_args()
    print(args)

