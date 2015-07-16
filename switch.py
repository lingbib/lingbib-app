#!/usr/bin/env python

"""
Usage:
  lingbib.py switch [options] (master | dbedit)
  lingbib.py --help
  
Options:
  -h --help         Show this help text and quit.
  -r --reset        Reset branch if it already exists (only for "dbedit").
"""

from __future__ import print_function

from lib.docopt import docopt
from lib.sh import git

from util import *
import config
import messages

__author__ =  "Kenneth Hanson"
__date__ =    "7/12/2015"


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)

    if not config.remote_upstream_url_is_set():
        config.set_remote_upstream_url()
        
    if config.unstaged_changes_exist():
        error(messages.UNSTAGED_CHANGES_ERROR)
        exit(1)

    if config.uncommitted_staged_changes_exist():
        error(messages.UNCOMITTED_STAGED_CHANGES_ERROR)
        exit(1)

    if args['master']:
        switch_to_master()
    elif args['dbedit']:
        if args["--reset"]:
            reset_dbedit_and_switch()
        else:
            if config.branch_dbedit_exists():
                prompt_to_reset_dbedit()
            else:
                create_dbedit_and_switch()
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing "
                        "without doing anything. Code has a logic error.")


def prompt_to_reset_dbedit():
    print(RESET_MSG)
    while True:
        try:
            line = raw_input("Please enter 'y' or 'n' (CTRL-D to cancel): ")
        except EOFError:
            break
        else:
            if line == 'y':
                switch_to_dbedit()
                break
            elif line == 'n':
                reset_dbedit_and_switch()
            else:
                continue

RESET_MSG = """\
Branch 'dbedit' already exists. If you have a pull request that is still open,
you can safely make additional modifications. If your last pull request is
closed, the branch should be deleted and recreated.
Is your last pull request still open?"""


def update_master():
    git.pull("--rebase", "upstream", "master")

def switch_to_dbedit():
    # TODO: confirm that this is really what we want
    # I don't think it will actually update "dbedit"
    update_master()
    git.checkout("dbedit")

def create_dbedit_and_switch():
    update_master()
    # create the new branch based on master and switch immediately
    git.checkout("-b", "dbedit", "master")

def reset_dbedit_and_switch():
    update_master()
    # delete remote branch
    git.push("origin", "--delete", "dbedit")
    # switch to branch, creating it if it doesn't exist
    git.checkout("-B", "dbedit", "master")


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name