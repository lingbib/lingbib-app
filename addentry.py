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
from subprocess import call

from lib.docopt import docopt

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


def addentry(argv):
    args = docopt(__doc__, argv=argv, help=True)

    # print(args)

    if args['FILE']:
        # run script in debug mode
        print("Calling scripts/addentry.sh with '{}'".format(args['FILE']))
        # call(['sh', '-n', 'scripts/addentry.sh', args['FILE']])
        raise NotImplementedError('Shell script not yet integrated.') 
    elif args['--interactive']:
        raise NotImplementedError('Interactive mode not yet implemented.')
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing"
                        "without doing anything. Code has a logic error.")


if __name__ == '__main__':
    addentry(sys.argv[1:]) # strip program name