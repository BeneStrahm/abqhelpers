# ------------------------------------------------------------------------------
# Description:  Helper functions for csv file handling
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      2020-09-16
# Execution:    Import functions / collections (from pylek.helpers import util)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
import csv
import os

# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def writeToCsv(fname, data, writeMode='a', cleanup=False):
    """Writing lines to .txt files
    :param fname: str w/ name of .txt file to write to
    :param data: list w/ text content
    :param writeMode: str w/ how to open file ('a', 'w')
    """
    if cleanup == True:
        # delete file if it exists
        if os.path.exists(fname):
            os.remove(fname)

    with open(fname, writeMode) as file:
        writer = csv.writer(file, delimiter='\t', lineterminator='\n')
        writer.writerows(data)
