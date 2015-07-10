#!/usr/bin/env python

"""
Usage:
  lingbib.py update [options] [PERSONAL_DB]
  lingbib.py update --help

Arguments:
  PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
  
Options:
  -h --help         Show this help text and quit.
  --debug           Allow code to be tested on branch "cli-dev".
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

    update_personal_db(pdb_path, debug_mode=args['--debug'])
    

def update_personal_db(personal_db_path, debug_mode=False):
    """
    Reimplementation of scripts/update_personal_db.sh.
    """
    info("Using '{db}' as personal database.".format(db=personal_db_path))
    
    # force the master branch to be used
    if debug_mode:
        debug("Currently on branch 'cli-dev'. Skipping switch to 'master'.")
    else:
        info("Not currently on 'master' branch. Switching now.")
        try:
            git.checkout("master")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to switch branches. "
                  "Please fix any Git problems and try again.")
            exit(1)

    # make sure upstream repo is set
    if not config.remote_upstream_url_set():
        info("Upstream repo not set. Setting now...")
        try:
            config.set_remote_upstream_url()
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set upstream repo."
                  " Please fix any Git problems and try again.")
            exit(1)
        else:
            info("Upstream repo set.")
    
    # fetch updates from upstream master
    if debug_mode:
        debug("Currently on branch 'cli-dev'. Skipping pull to 'master'.")
    else:
        info("Pulling updates to master database...")
        try:
            git.pull("--rebase upstream master".split())
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Please run 'git pull --rebase upstream master' and resolve "
                  "the conflicts, then try again.")
            exit(1)
        else:
            info("Update complete.")


    # invoke bibtool to merge master and personal databases, overwriting personal
    info("Merging master database with personal database.")
    cmd_status = bibtool("-r", "bibtool/personal-merge.rsc", personal_db_path, defaults.DB_MASTER, o=personal_db_path)
    if cmd_status.stdout != "":
        info(cmd_status.stdout)
    # bibtool doesn't return a non-zero exit code for bad filenames,
    #   so for now check if stdout and stderr are nonempty and print manually
    if cmd_status.stderr != "":
        error("Call to Bibtool failed.")
        error(cmd_status.stderr)
    else:
        info("Merge complete.")


if __name__ == '__main__':
  main(sys.argv[1:]) # strip program name