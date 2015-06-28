#!/usr/bin/env python

"""
Usage:
  lingbib.py config [options] check
  lingbib.py config set
  lingbib.py --help
  
Options:
  -a --auto  Take all defaults.
  -h --help  Show this help text and quit.

Origin is your personal repository.
Upstream is the lingbib repo.
Links are symlinks to the bibliography files.
"""

from __future__ import print_function

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

    if args['--auto']:
        raise NotImplementedError("'--auto' option not implemented.")
    
    if args["check"]:
        check_all()
    elif args["set"]:
        raise NotImplementedError("'set' subcommand not implemented.")


#
# Functions for reporting on local settings
#

results = {True : "OK", False: "***NO***"}

def config_test(description, test_func):
    result = test_func()
    print(description + "..." + results[result])
    return result

def check_all():
    num_failed = 0
    num_failed += config_test("Branch 'master' exists", master_branch_exists)
    num_failed += config_test("Branch 'bib-edit' exists", bibedit_branch_exists)
    num_failed += config_test("Remote repo 'origin' set to personal repo",
                              remote_origin_url_set)
    num_failed += config_test("Remote repo 'upstream' set to lingbib repo",
                              remote_upstream_url_set)

    if using_ssh_urls():
        warning("Currently configured to use SSH URL(s). This may not work"
                " if SSH is not configured appropriately.")
    if num_failed > 0:
        warning("One or more tests failed.")


#
# query functions
#

def master_branch_exists():
    return 'master' in git.branch()

def bibedit_branch_exists():
    return 'bibedit' in git.branch()

def remote_origin_url():
    try:
        return git.config("remote.origin.url")
    except sh.ErrorReturnCode:
        return None

def remote_origin_url_set():
    return remote_origin_url() != None

def remote_upstream_url():
    try:
        return git.config("remote.upstream.url")
    except sh.ErrorReturnCode:
        return None

def remote_upstream_url_set():
    return remote_upstream_url().strip() in UPSTREAM_URLS.values()

def using_ssh_urls():
    try:
        return "git@github" in git.remote("-v")
    except sh.ErrorReturnCode:
        return False


#
# setter functions
#

# def set_master():
#     if not 'upstream' in git.remote():
#         out = git.remote.add("upstream", "https://github.com/lingbib/lingbib.git")
#         print(out)

def set_remote_upstream_url():
    git.remote.add("upstream", "https://github.com/lingbib/lingbib.git")


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name