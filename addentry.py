#!/usr/bin/env python

"""
Usage:
  lingbib.py addentry [options] FILE
  lingbib.py addentry [options] (-i | --interactive)
  lingbib.py --help

Arguments:
  FILE  File containing new entries to process.
  
Options:
  -i --interactive  Opens the default editor for quick data entry,
                      on systems where this feature exists.
  -h --help         Show this help text and quit.
"""

from __future__ import print_function

from lib.docopt import docopt
from lib.sh import bibtool
from lib.sh import git

import defaults
from util import *

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)

    if args['FILE'] is not None:
        addentry(args['FILE'])
    elif args['--interactive']:
        raise NotImplementedError('Interactive mode not yet implemented.')
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing"
                        "without doing anything. Code has a logic error.")

def addentry(filepath):
    # autogen keys
    bibtool('-r', "bibtool/keygen.rsc", filepath, o=filepath)

    # merge with master database
    bibtool("-r", "bibtool/sanitize.rsc", filepath, defaults.DB_MASTER, o=defaults.DB_MASTER)

    # Update macro and refs file
    bibtool("-r", "bibtool/ref-extraction.rsc", defaults.DB_MASTER, o="MacrosAndRefs.txt")

    # Then stage the new changes
    git.add(defaults.DB_MASTER)


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name