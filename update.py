#!/usr/bin/env python

"""
Usage:
  lingbib.py update [options] [PERSONAL_DB]
  lingbib.py update --help

Arguments:
  PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
  
Options:
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
import defs
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
        pdb_path = defs.DB_PERSONAL
    update_personal_db(pdb_path, skip_backup=args['--nobackup'])
    

def update_personal_db(personal_db_path, skip_backup):
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
    if not config.current_branch() == defs.BRANCH_MASTER:
        info("Not currently on 'master' branch. Switching now.")
        try:
            git.checkout("master")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to switch branches. "
                  "Please fix any Git problems and try again.")
            exit(1)

    # make sure remote 'lingbib' is set
    if not config.remote_lingbib_url_is_set():
        config.set_remote_lingbib_url()
    
    # fetch updates from lingbib/master
    info("Pulling updates to master database...")
    try:
        git.pull("--rebase lingbib master".split())
    except sh.ErrorReturnCode as e:
        error(e.stderr)
        error("Please run 'git pull --rebase lingbib master' and resolve "
              "the conflicts, then try again.")
        exit(1)
    else:
        info("Update complete.")

    # fetch updates from remote "personal"
    # TODO
    
    # backup current personal bibfile
    if not skip_backup:
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
        personal_db_path, defs.DB_MASTER, o=personal_db_path,
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