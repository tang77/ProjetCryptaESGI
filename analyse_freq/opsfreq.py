#! /usr/bin/env python
#coding: utf-8

#IMPORTS
from misc import generic_ops 
import copy
import math

def get_stats_from_file(file_in, n):
    tmp = dict()
    with open(file_in, mode='r') as fop:
        bufline = fop.read().splitlines()
        for phrase in bufline:
            for word in phrase.split(' '):
                word = generic_ops.suppr_bad_chars(word).upper()
                if len(word) >= n:
                    generic_ops.count_n_gram(word, tmp, n)
    return convert_to_freq(tmp)

def convert_to_freq(freq_dict):
    total = float(sum(freq_dict.itervalues()))
    return dict((k,float(str(round(float(v)/total*100.0,4)).format('{.4f}'))) for k,v in freq_dict.iteritems())


def decipher(cipher):
    global freq_un
    global freq_bi
    global freq_tri
    tmp = dict()

    buf = cipher.upper().split(" ")

    # matching monogramme
    for word in buf:
        word = generic_ops.suppr_bad_chars(word)
        generic_ops.count_n_gram(word, tmp, 1)

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
