#!/usr/bin/env python

"""
Usage:
  lingbib.py config check
  lingbib.py config dump
  lingbib.py config setdefaults
  lingbib.py --help

Subcommands:
  check        check that local repository is set up correctly
  dump         display relevant raw Git configuration data for debugging
  setdefaults  set relevant Git configuration to default values

Options:
  -h --help  Show this help text and quit.
"""

from __future__ import print_function
import sys

from lib.docopt import docopt
from lib import sh
from lib.sh import git

from util import *
from defs import *

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


LINGBIB_URLS = {"http":      "http://github.com/lingbib/lingbib",
                 "http.git":  "http://github.com/lingbib/lingbib.git",
                 "https":     "https://github.com/lingbib/lingbib",
                 "https.git": "https://github.com/lingbib/lingbib.git",
                 "ssh":       "git@github.com:lingbib/lingbib",
                 "ssh.git":   "git@github.com:lingbib/lingbib.git"}


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)
    
    if args["check"]:
        check_all()
    elif args["dump"]:
        dump()
    elif args["setdefaults"]:
        set_defaults()


#
# Functions for reporting configuration
#

RESULTS = {True : "   OK   ", False: "***NO***"}

def config_test(description, test_func, expected_val=None):
    """Run test and print results. Return 0 if result OK, 1 otherwise."""
    result = test_func()
    print("{desc}: {res}".format(desc=description, res=RESULTS[result]))
    return 0 if result is True else 1

def check_all():
    num_failed = 0
    num_failed += config_test("Branch 'master' exists                      ",
                              branch_master_exists)
    num_failed += config_test("Branch 'master' tracking remote 'personal'  ",
                              branch_master_tracking_personal)
    num_failed += config_test("Remote repo 'lingbib' set to official repo  ",
                              remote_lingbib_url_is_set)
    num_failed += config_test("Remote repo 'personal' set to personal repo ",
                              remote_personal_url_is_set)
    if num_failed > 0:
        warning("One or more tests failed."
                " Run `lingbib.py config dump` to see the relevant settings.")
    if using_ssh_urls():
        warning("Currently configured to use SSH URL(s). This may not work"
                " if SSH is not configured appropriately.")

def dump():
    """Print raw config info."""
    print("-----Git Branches-----")
    git.branch("-vv", _out=gitout)

    print()
    print("-----Git Remotes-----")
    git.remote("-v", "show", _out=gitout)


#
# query functions
#

def current_branch():
    return git("rev-parse", "--abbrev-ref", "HEAD").strip()

def branch_master_exists():
    return BRANCH_MASTER in git.branch()

def branch_master_tracking_personal():
    try:
        return REMOTE_PERSONAL in git.config("branch.master.remote")
    except sh.ErrorReturnCode:
        return False

def branch_dbedit_exists():
    return BRANCH_DBEDIT in git.branch()

def remote_personal_dbedit_exists():
    return REMOTE_PERSONAL_DBEDIT in git.branch("-r")
    
def remote_personal_url():
    try:
        return git.config("remote.personal.url").strip()
    except sh.ErrorReturnCode:
        return None

def remote_personal_url_is_set():
    url = remote_personal_url()
    if url is None:
        return False
    else:
        return url not in LINGBIB_URLS.values()

def remote_lingbib_url():
    try:
        return git.config("remote.lingbib.url").strip()
    except sh.ErrorReturnCode:
        return None

# TODO: decide whether to switch to substring matching
#   for "github.com" and "lingbib/lingbib"
def remote_lingbib_url_is_set():
    url = remote_lingbib_url()
    if url is None:
        return False
    else:
        return url in LINGBIB_URLS.values()

def using_ssh_urls():
    try:
        return "git@github" in git.remote("-v")
    except sh.ErrorReturnCode:
        return False

def unstaged_changes_exist():
    try:
        git("diff-files", "--quiet")
    except sh.ErrorReturnCode:
        return True
    else:
        return False

def uncommitted_staged_changes_exist():
    try:
        git("diff-index", "--quiet", "--cached", "HEAD")
    except sh.ErrorReturnCode:
        return True
    else:
        return False


#
# setter functions
#

def set_defaults():
    if not remote_personal_url_is_set():
        warning("Remote 'personal' not set. "
                "Please set it to your personal fork manually.")
        warning("Skipping other settings that depend on this.")
    else:
        if not branch_master_exists():
            git.checkout("master", "remote/personal")
        elif not branch_master_tracking_personal():
            set_branch_master_tracking()

    if not remote_lingbib_url_is_set():
        set_remote_lingbib_url()


def set_branch_master_tracking():
    """Set branch 'master' to track remote 'personal'.

    Should only be called if the URL for 'personal' is set.
    """
    if branch_master_tracking_personal():
        info("Branch 'master' already tracking 'personal'.")
    else:
        try:
            # start by fetching, since Git won't set the upstream repo
            # for a branch if there isn't a local copy yet
            git.fetch("personal")
            git.branch("--set-upstream-to", REMOTE_PERSONAL_MASTER, "master")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set tracking for branch 'master'."
                  " Please fix any Git problems and try again.")
            exit(1)
        else:
            info("Master branch set to track personal repo.")


def set_remote_lingbib_url():
    if remote_lingbib_url_is_set():
        info("Remote repo 'lingbib' already set.")
    else:
        info("Setting remote repo 'lingbib' now...")
        try:
            git.remote.add("lingbib", "https://github.com/lingbib/lingbib.git")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set remote repo 'lingbib'."
                  " Please fix any Git problems and try again.")
            exit(1)
        else:
            info("Remote repo 'lingbib' set.")
    

# def test():
#     check_all()


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name
