#!/usr/bin/env python

"""
Usage:
  lingbib.py update [options] [PERSONAL_DB]
  lingbib.py update --help

Arguments:
  PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
  
Options:
  --debug        Make code work on "cli-dev" by skipping branch change.
  -h --help      Show this help text and quit.
  -n --nobackup  Don't make a backup of the personal bibfile.
"""

from __future__ import print_function
import sys
import os

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

    if args['--debug']:
        debug("***Debug mode enabled.***")
    update_personal_db(pdb_path, debug_mode=args['--debug'])
    

def update_personal_db(personal_db_path, debug_mode=False):
    """
    Reimplementation of scripts/update_personal_db.sh.
    """
    # ensure that personal database exists
    if os.path.isfile(personal_db_path):
        info("Using '{db}' as personal database.".format(db=personal_db_path))
    else:
        error("Personal database '{db}' does not exist.".format(
              db=personal_db_path))
        exit(1)

    # force the master branch to be used
    if debug_mode:
        debug("Skipping switch to branch 'master'.")
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
        debug("Skipping pull to branch 'master'.")
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

    # backup current personal bibfile
    backup_path = personal_db_path + ".old"
    try:
        sh.cp(personal_db_path, backup_path)
    except sh.ErrorReturnCode as e:
        error("Unable to make a backup of the current personal database.")
        error(e.stderr)
        exit(1)
    else:
        info("Backed up current personal database as '{old}'.".format(
             old=backup_path))

    # invoke BibTool to merge master and personal databases, overwriting personal
    # Note: BibTool considers things that should be errors as warnings, and
    #   doesn't return an error code so for now just print warnings
    info("Merging master database with personal database.")
    try:
        cmd_status = bibtool("-r", "bibtool/personal-merge.rsc",
        personal_db_path, defaults.DB_MASTER, o=personal_db_path,
        _out=handle_bibtool_output, _err=handle_bibtool_output)
    except sh.ErrorReturnCode as e:
        error("Call to BibTool failed.")
        error(e.stderr)
        exit(1)


def handle_bibtool_output(line):
    if line != "":
        print(line)


if __name__ == '__main__':
  main(sys.argv[1:]) # strip program name