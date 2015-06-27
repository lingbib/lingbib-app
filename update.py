#!/usr/bin/env python

"""
Usage:
  lingbib.py update [options] [PERSONAL_DB]
  lingbib.py --help

Arguments:
  PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
  
Options:
  -h --help         Show this help text and quit.

"""

from __future__ import print_function
from subprocess import call
import sys

from lib.docopt import docopt

__author__ =  "Kenneth Hanson"
__date__ =    "6/23/2015"


def main(argv):
    args = docopt(__doc__, argv=argv, help=True)

    # print(args)

    db = args['PERSONAL_DB']
    if db == None:
        db = "lingbib-personal.bib"

    # run script in debug mode
    # call(['sh', '-n', 'scripts/update_personal_db.sh', db])
    print("Calling scripts/update_personal_db.sh with '{}'".format(db))
    print("TODO: fix script so that it can be called properly")

if __name__ == '__main__':
  main(sys.argv)