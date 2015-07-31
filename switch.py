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
from defaults import *
import config
import messages

__author__ =  "Kenneth Hanson"
__date__ =    "7/12/2015"


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)

    # ensure that current branch is clean
    if config.unstaged_changes_exist():
        error(messages.UNSTAGED_CHANGES_ERROR)
        exit(1)

    if config.uncommitted_staged_changes_exist():
        error(messages.UNCOMITTED_STAGED_CHANGES_ERROR)
        exit(1)

    if args['master']:
        switch_to_master()
    elif args['dbedit']:
        switch_to_dbedit(do_reset=args["--reset"])
        
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing "
                        "without doing anything. Code has a logic error.")


def switch_to_master():
    if config.current_branch() == BRANCH_MASTER:
        print("Already on branch 'master'.")
    else:
        cmd = git.checkout("master", _out=gitout)


def switch_to_dbedit(do_reset=False):
    if config.current_branch() == BRANCH_DBEDIT:
        print("Already on branch 'dbedit'.")
        return

    # fetch updates
    if not config.remote_lingbib_url_is_set():
        config.set_remote_lingbib_url()
    fetch_lingbib()

    if do_reset:
        reset_dbedit_and_switch()
    else:
        if config.branch_dbedit_exists():
            prompt_to_reset_dbedit()
        else:
            create_dbedit_and_switch()

def prompt_to_reset_dbedit():
    print(RESET_MSG)
    while True:
        try:
            line = raw_input("Please enter 'y' or 'n' (CTRL-D to cancel): ")
        except EOFError:
            break
        else:
            if line == 'y':
                update_dbedit_and_switch()
                break
            elif line == 'n':
                reset_dbedit_and_switch()
                break
            else:
                continue

RESET_MSG = """\
Branch 'dbedit' already exists. If you have a pull request that is still open,
you can safely make additional modifications. If your last pull request is
closed, the branch should be deleted and recreated.
Do you want to reuse the existing branch?"""


def fetch_lingbib():
    info("Fetching updates from remote 'lingbib'...")
    try:
        git.fetch(REMOTE_LINGBIB)
    except sh.ErrorReturnCode as e:
        error("Unable to fetch updates.")
    else:
        info("Up to date.")

def update_dbedit_and_switch():
    git.checkout(BRANCH_DBEDIT, _out=gitout)
    git.rebase("lingbib/master", _out=gitout)

def create_dbedit_and_switch():
    """create the new branch based on master and switch immediately"""
    git.checkout("-b", BRANCH_DBEDIT, "lingbib/master", _out=gitout)

def reset_dbedit_and_switch():
    # delete remote branch, if applicable
    if config.remote_personal_dbedit_exists():
        try:
            git.push(REMOTE_PERSONAL, "--delete", BRANCH_DBEDIT)
        except sh.ErrorReturnCode as e:
            error(e)
            error("Unable to delete the remote branch.")

    # switch to branch, creating it if it doesn't exist
    git.checkout("-B", BRANCH_DBEDIT, "lingbib/master", _out=gitout)


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name