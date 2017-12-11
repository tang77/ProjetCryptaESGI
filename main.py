#! /usr/bin/env python
#coding: utf-8

#IMPORTS
import sys
from collections import Counter
from misc import testing_module_msc 
from misc import generic_ops 
from analyse_freq import opsfreq 

def main():
    print "That's a main"
    testing_module_msc.testing()
    print "[*] Build stats from dictionnary... Please wait!\n"

    dictionnaire = "others/bigdic.txt"
    global freq_un
    freq_un = opsfreq.get_stats_from_file(dictionnaire, 1)

    global freq_bi
    freq_bi = opsfreq.get_stats_from_file(dictionnaire, 2)

    global freq_tri
    freq_tri = opsfreq.get_stats_from_file(dictionnaire, 3)

    print "[*] Building finished...\n"

    print "[*] TOP 5 - Monogramme"
    print Counter(freq_un).most_common(5)

    print "[*] TOP 5 - Bigramme"
    print Counter(freq_bi).most_common(5)

    print "[*] TOP 5 - Trigramme"
    print Counter(freq_tri).most_common(5)

    print "\n[*] Done!\n"

    cipher = raw_input("[*] Please enter your ciphered text here:\n>")
    opsfreq.decipher(cipher)


if __name__ == "__main__":
    main()
