#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: reducer.py
Created: 2018-12-07

Description:
    reduce a set of incoming (key, value) to be the key followed by the maximum
    value

Usage:

    test with

        cat usaspending_test.csv | python mapper.py | sort | python reducer.py

    run with

        cat my_usaspending_file.csv | python mapper.py | sort | python reducer.py

"""

import sys

from itertools import groupby


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #


# ----------------------------- #
#   key-value emitter           #
# ----------------------------- #

def reduce():
    """our inputs now are key-value pairs where the key is the two unique ids
    for a contract (as a ','-separated string) and the values are 1 or 0
    (depending on whether or not an action for that key was a termination). the
    reducer seeks to find the maximum value (1 if any was a termination, 0 only
    if none were terminations)

    """
    # make an iterator which just splits each incoming row into keys and values
    kvp_iter = (row.strip().split('\t') for row in sys.stdin)

    # make a groupby iterator for chunking up the kvp_iter item by key
    grouped_iter = groupby(kvp_iter, key=lambda kvp: kvp[0])

    for (key, keyvallist) in grouped_iter:
        # the grouped_iter above is a little fancy and weird. basically, the
        # keyvallist is itself a list of elements where each element is a tuple.
        # the first element of the tuple is the current key (yes, it's redundant
        # with the key we've already identified in the `for` statemenet above)
        # and the second element is the value in the original record. this means
        # that a keyvallist would look like
        #
        #   [('award_id_piid,parent_award_id', '0'),
        #    ('award_id_piid,parent_award_id', '0'),
        #    ('award_id_piid,parent_award_id', '1'),
        #    ('award_id_piid,parent_award_id', '0')]
        #
        # our goal is to identify the maximum value among the second elements in
        # this list
        max_keyval = max(
            keyvallist,
            key=lambda keyval: int(keyval[1]))
        _, maxval = max_keyval

        # emit a string that is award_id_piid,parent_award_id,maxval
        print('{},{}'.format(key, maxval))


if __name__ == '__main__':
    reduce()
