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
from lib import sh
from lib.sh import git
from lib.sh import bibtool

from util import *
import defaults
import config

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)

    pdb_path = args['PERSONAL_DB']
    if pdb_path == None:
        pdb_path = defaults.DB_PERSONAL

    update_personal_db(pdb_path)
    

def update_personal_db(personal_db_path, any_branch=False):
    """
    Reimplementation of scripts/update_personal_db.sh.
    """
    info("Using '{db}' as personal database.".format(db=personal_db_path))
    
    # force the master branch to be used
    # try:
    #     git.checkout("master")
    # except sh.ErrorReturnCode as e:
    #     error(e.stderr)
    #     error("Please fix any problems and switch to the master branch manually.")
    #     exit(1)

    # make sure upstream repo is set
    if not config.remote_upstream_url_set():
        info("Upstream repo not set. Setting now...")
        try:
            config.set_remote_upstream_url()
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set upstream repo.")
            exit(1)
        else:
            info("Upstream repo set.")
    
    # fetch updates from upstream master
    # try:
    #     git.pull("--rebase upstream master".split())
    # except sh.ErrorReturnCode as e:
    #     error(e.stderr)
    #     error("Please run 'git pull --rebase upstream master' and resolve the \
    #            conflicts. Then you can rerun this script to update your personal \
    #            copy of the database")
    #     exit(1)

    # invoke bibtool to merge master and personal databases, overwriting personal
    out = bibtool("-r", "bibtool/personal-merge.rsc", personal_db_path, defaults.DB_BIBLATEX_MASTER, o=personal_db_path)
    print(defaults.DB_BIBLATEX_MASTER, personal_db_path, out)


if __name__ == '__main__':
  main(sys.argv[1:]) # strip program name