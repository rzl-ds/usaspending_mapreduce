#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: mapper.py
Created: 2018-12-07

Description:
    map a line in usaspending csvs to a key-value pair with
    (parent_award_id, award_id_piid) as key and a boolean (0, 1) indicating
    whether or not that line is a termination action as the value

Usage:
    test with

        cat usaspending_test.csv | python mapper.py

    run with

        cat my_usaspending_file.csv | python mapper.py

"""

import csv
import sys


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

AWARD_ID_PIID = 2
PARENT_AWARD_ID = 7
ACTION_TYPE = 78
RECORD_LENGTH = 277

BAD_ACTION_TYPES = [
    'TERMINATE FOR DEFAULT (COMPLETE OR PARTIAL)',
    'TERMINATE FOR CAUSE',
]


# ----------------------------- #
#   key-value emitter           #
# ----------------------------- #

def map():
    """our mapper is very simple. we will start by attempting to parse every
    line into a 277 element list. we will then emit key-value pairs where the
    keys are the 0th and 3rd elements (the `award_id_piid` and
    `parent_award_id`, respectively), and the value is a boolean (0, 1)
    indicating whether or not that record's `action_type` (element 77) was of a
    "bad" type (1 if it is a bad type, 0 if it is not)

    """
    # we use a csv.reader object to handle the quoted commas -- easier than
    # just splitting on them. same for the ouptut record, which is equally hard.
    # also, no point in handling the \n characters mid-line, because *hadoop*
    # will only split on \n characters, so the lines we get will already be
    # busted. just throw away the busted lines.
    csv_in = csv.reader(sys.stdin)

    for (i, rec) in enumerate(csv_in):
        # ignore the header line
        if i == 0 and rec[0] == 'award_id_piid':
            continue

        # skip records that don't have the proper length
        if len(rec) != RECORD_LENGTH:
            continue

        # the key is the tuple of award_id_piid and parent_award_id
        key = rec[AWARD_ID_PIID], rec[PARENT_AWARD_ID]

        # the value is a boolean on the action_type
        value = int(rec[ACTION_TYPE] in BAD_ACTION_TYPES)

        # we return the kvp by printing it back to stdout as a \t separated
        # pair. this means we need to concatenate the key somehow, and we
        # do that by printing it as a comman-separated pair here:
        print('{},{}\t{}'.format(key[0], key[1], value))


if __name__ == '__main__':
    map()
