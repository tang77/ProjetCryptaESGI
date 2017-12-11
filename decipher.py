#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import heapq
import math
import copy
from collections import Counter

reload(sys)
sys.setdefaultencoding('utf8')

freq_un = dict()
freq_bi = dict()
freq_tri = dict()

def get_n_word(text, size):
    return [text[i:i+size] for i in range(0, len(text), size)]

def count_n_gram(text, dico, n):
    for n_gram in get_n_word(text, n):
        if len(n_gram) >= n:
            if n_gram in dico:
                dico[n_gram] += 1
            else:
                dico[n_gram] = 1

def convert_to_freq(freq_dict):
    total = float(sum(freq_dict.itervalues()))
    return dict((k,float(str(round(float(v)/total*100.0,4)).format('{.4f}'))) for k,v in freq_dict.iteritems())

def get_stats_from_file(file_in, n):
    tmp = dict()
    with open(file_in, mode='r') as fop:
        bufline = fop.read().splitlines()
        for phrase in bufline:
            for word in phrase.split(' '):
                word = suppr_bad_chars(word).upper()
                if len(word) >= n:
                    count_n_gram(word, tmp, n)
    return convert_to_freq(tmp)

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

def decipher(cipher):
    global freq_un
    global freq_bi
    global freq_tri
    tmp = dict()
    
    buf = cipher.upper().split(" ")
    
    # matching monogramme
    for word in buf:
        word = suppr_bad_chars(word)
        count_n_gram(word, tmp, 1)

    tmp = convert_to_freq(tmp)
    tmp2 = copy.deepcopy(freq_un)

    while len(tmp2) > 0:
        key = ''
        for k in tmp2:
            old = min(tmp, key=lambda x:math.fabs(tmp[x]-tmp2[k]))
            print k, ' => ', old
            cipher = cipher.replace(old, k)
            key = k
            break
        tmp2.pop(key, None)


    print cipher

def main():
    print "[*] Build stats from dictionnary... Please wait!\n"

    dictionnaire = "bigdic.txt"
    global freq_un
    freq_un = get_stats_from_file(dictionnaire, 1)

    global freq_bi
    freq_bi = get_stats_from_file(dictionnaire, 2)

    global freq_tri
    freq_tri = get_stats_from_file(dictionnaire, 3)

    print "[*] TOP 5 - Monogramme"
    print Counter(freq_un).most_common(5)

    print "[*] TOP 5 - Bigramme"
    print Counter(freq_bi).most_common(5)

    print "[*] TOP 5 - Trigramme"
    print Counter(freq_tri).most_common(5)

    print "\n[*] Done!\n"

    cipher = raw_input("[*] Please enter your ciphered text here:\n>")
    decipher(cipher)

main()