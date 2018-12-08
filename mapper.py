#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: mapper.py
Created: 2018-12-07

Description:
    map a line in usaspending csvs to a key-value pair with
    (parent_award_id, award_id_piid) as key and the input text line as value

Usage:
    test with

        cat usaspending_test.csv | python mapper.py

    run with

        cat my_usaspending_file.csv | python mapper.py

"""

import csv
import os
import sys

from StringIO import StringIO


# ----------------------------- #
#   Module Constants            #
# ----------------------------- #

HERE = os.path.dirname(os.path.realpath(__file__))
TEST_FILE = os.path.join(HERE, 'usaspending_test.csv')


# ----------------------------- #
#   key-value emitter           #
# ----------------------------- #

def map():
    """take each input line in the csv and parse it into a 261 element list.
    emit key-value pairs where the keys are the 0th and 3rd elements (the
    `award_id_piid` and `parent_award_agency_id`, respectively), and values are
    the original line

    """
    # we use a csv.reader object to handle the quoted commans -- easier than
    # just splitting on them. same for the ouptut record, which is equally hard
    csv_in = csv.reader(sys.stdin)

    sio_out = StringIO()
    csv_out = csv.writer(sio_out)

    for (i, rec) in enumerate(csv_in):
        # ignore the header line
        if i == 0 and rec[0] == 'award_id_piid':
            continue

        # the key is the 0 and 3 element of that record
        key = rec[0], rec[3]

        # the value is the line itself, re-joined and properly quoted -- no easy
        # feat!
        line_out = StringIO()
        writer = csv.writer(line_out)
        writer.writerow(rec)
        value = line_out.getvalue().strip()

        print('{},{}\t{}'.format(key[0], key[1], value))


if __name__ == '__main__':
    map()
