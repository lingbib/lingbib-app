#!/usr/bin/env python

"""
Usage:
  lingbib.py update [options] [PERSONAL_DB]
  lingbib.py update --help

Arguments:
  PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
  
Options:
  -h --help         Show this help text and quit.
"""

from __future__ import print_function
import sys

from lib.docopt import docopt

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


def update(argv):
    args = docopt(__doc__, argv=argv, help=True)

    db = args['PERSONAL_DB']
    if db == None:
        db = "lingbib-personal.bib"

    # run script in debug mode
    # call(['sh', '-n', 'scripts/update_personal_db.sh', db])
    print("Calling scripts/update_personal_db.sh with '{}'".format(db))
    raise NotImplementedError('Shell script not yet integrated.') 


if __name__ == '__main__':
  addentry(sys.argv[1:]) # strip program name