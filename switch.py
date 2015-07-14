#!/usr/bin/env python

"""
Usage:
  lingbib.py switch (master | dbedit)
  lingbib.py --help
  
Options:
  -h --help         Show this help text and quit.
"""

from __future__ import print_function

from lib.docopt import docopt
from lib.sh import git

from util import *
import config

__author__ =  "Kenneth Hanson"
__date__ =    "7/12/2015"


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)
    debug(args)

    if args['master']:
        git.checkout("master")
    elif args['dbedit']:
        # NOTE: this will reset 'dbedit' every time, which needs to be changed
        #   in the future
        git.checkout("-B", "dbedit")
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing"
                        "without doing anything. Code has a logic error.")


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name