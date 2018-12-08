#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: reducer.py
Created: 2018-12-07

Description:
    reduce a set of incoming (key, value) pairs to only the most recent value
    (as determined by the last_modified_date field, the last field in each
    incoming record)

Usage:

    test with

        cat usaspending_test.csv | python mapper.py | sort | python reducer.py

    run with

        cat my_usaspending_file.csv | python mapper.py | sort | python reducer.py

"""

import os
import sys

from itertools import groupby


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))


# ----------------------------- #
#   key-value emitter           #
# ----------------------------- #

def reduce():
    """our inputs now are key-value pairs where the key is the two unique ids
    for a contract and the values are the lines which have those ids. we may get
    more than one key per run of the reducer so we have to chunk the input up by
    input key

    """
    # make an iterator which just splits each incoming row into keys and values
    kvp_iter = (row.strip().split('\t') for row in sys.stdin)

    # make a groupby iterator for chunking up the kvp_iter item by key
    grouped_iter = groupby(kvp_iter, key=lambda kvp: kvp[0])

    for (key, keyvallist) in grouped_iter:
        # the keyvallist is a list of elements where each element is the current
        # key (yes, it's redundant with the key we've already identified in the
        # `for` statemenet above) and the line
        max_keyval = max(keyvallist, key=lambda keyval: keyval[1].split(',')[-1])
        _, maxval = max_keyval
        print(maxval)


if __name__ == '__main__':
    reduce()
