#!/usr/bin/env python

"""
Usage:
  lingbib.py config [options] (origin | upstream | links | all)
  lingbib.py --help
  
Options:
  -a --auto  Take all defaults.
  -h --help  Show this help text and quit.

Origin is your personal repository.
Upstream is the lingbib repo.
Links are symlinks to the bibliography files.
"""

from __future__ import print_function
from subprocess import call
import os

from lib.docopt import docopt
from lib.sh import git

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


def config(argv):
    args = docopt(__doc__, argv=argv, help=True)

    if args['--auto']:
        raise NotImplementedError('Shell script not yet integrated.') 
    else:
        check()


def check():
    pass
    # out = git("branch")
    # print(out)

if __name__ == '__main__':
    addentry(sys.argv[1:]) # strip program name