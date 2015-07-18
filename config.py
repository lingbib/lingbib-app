#!/usr/bin/env python

"""
Usage:
  lingbib.py config check
  lingbib.py config setdefaults
  lingbib.py --help
  
Options:
  -h --help  Show this help text and quit.

Origin is your personal repository.
Upstream is the lingbib repo.
Links are symlinks to the bibliography files.
"""

from __future__ import print_function
import sys

from lib.docopt import docopt
from lib import sh
from lib.sh import git

from util import *

__author__ =  "Kenneth Hanson"
__date__ =    "6/27/2015"


UPSTREAM_URLS = {"https" : "https://github.com/lingbib/lingbib.git",
                 "ssh" : "git@github.com:lingbib/lingbib"}


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, help=True)
    
    if args["check"]:
        check_all()
    elif args["setdefaults"]:
        set_defaults()


#
# Functions for reporting configuration
#

results = {True : "OK", False: "***NO***"}

def config_test(description, test_func):
    result = test_func()
    print(description + "..." + results[result])
    return result

def check_all():
    num_failed = 0
    num_failed += config_test("Branch 'master' exists", branch_master_exists)
    num_failed += config_test("Branch 'master' tracking remote 'origin'", branch_master_tracking_origin)
    # num_failed += config_test("Branch 'dbedit' exists", branch_dbedit_exists)
    num_failed += config_test("Remote repo 'origin' set",
                              remote_origin_url_is_set)
    num_failed += config_test("Remote repo 'origin' is not lingbib/lingbib",
                              remote_origin_url_is_not_upstream_repo)
    num_failed += config_test("Remote repo 'upstream' set to lingbib repo",
                              remote_upstream_url_is_set)
    if num_failed > 0:
        warning("One or more tests failed.")
    if using_ssh_urls():
        warning("Currently configured to use SSH URL(s). This may not work"
                " if SSH is not configured appropriately.")


#
# query functions
#

def branch_master_exists():
    return 'master' in git.branch()

def branch_master_tracking_origin():
    return 'origin' in git.config("branch.master.remote")

def branch_dbedit_exists():
    return 'dbedit' in git.branch()

def remote_origin_dbedit_exists():
    return 'dbedit' in git.branch("-r")
    
def remote_origin_url():
    try:
        return git.config("remote.origin.url")
    except sh.ErrorReturnCode:
        return None

def remote_origin_url_is_set():
    return remote_origin_url() is not None

def remote_origin_url_is_not_upstream_repo():
    url = remote_origin_url()
    if url is None:
        return True
    else:
        return url.strip() not in UPSTREAM_URLS.values()

def remote_upstream_url():
    try:
        return git.config("remote.upstream.url")
    except sh.ErrorReturnCode:
        return None

def remote_upstream_url_is_set():
    url = remote_upstream_url()
    if url is None:
        return False
    else:
        return url.strip() in UPSTREAM_URLS.values()

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
    if not remote_origin_url_is_set():
        warning("Remote 'origin' not set. "
                "Please set it to your personal fork manually.")
        warning("Skipping other settings that depend on this.")
    else:
        if not branch_master_exists():
            git.checkout("master", "remote/origin")
        elif not branch_master_tracking_origin():
            set_branch_master_tracking()

    if not remote_upstream_url_is_set():
        set_remote_upstream_url()


def set_branch_master_tracking():
    if branch_master_tracking_origin():
        info("Branch 'master' already tracking origin.")
    else:
        try:
            git.branch("--set-upstream-to", "origin/master", "master")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set tracking for branch 'master'."
                  " Please fix any Git problems and try again.")
            exit(1)
        else:
            info("Upstream repo set.")


def set_remote_upstream_url():
    if remote_upstream_url_is_set():
        info("Upstream repo already set.")
    else:
        info("Setting upstream repo now...")
        try:
            git.remote.add("upstream", "https://github.com/lingbib/lingbib.git")
        except sh.ErrorReturnCode as e:
            error(e.stderr)
            error("Unable to set upstream repo."
                  " Please fix any Git problems and try again.")
            exit(1)
        else:
            info("Upstream repo set.")
    

# def test():
#     check_all()


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name
