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
    num_failed += config_test("Branch 'master' exists", branch_master_exists)
    num_failed += config_test("Branch 'dbedit' exists", branch_dbedit_exists)
    num_failed += config_test("Remote repo 'origin' set to personal repo",
                              remote_origin_url_is_set)
    num_failed += config_test("Remote repo 'upstream' set to lingbib repo",
                              remote_upstream_url_is_set)

    if using_ssh_urls():
        warning("Currently configured to use SSH URL(s). This may not work"
                " if SSH is not configured appropriately.")
    if num_failed > 0:
        warning("One or more tests failed.")


#
# query functions
#

def branch_master_exists():
    return 'master' in git.branch()

def branch_dbedit_exists():
    return 'dbedit' in git.branch()

def remote_origin_url():
    try:
        return git.config("remote.origin.url")
    except sh.ErrorReturnCode:
        return None

def remote_origin_url_is_set():
    return remote_origin_url() is not None

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

# def set_master():
#     if not 'upstream' in git.remote():
#         out = git.remote.add("upstream", "https://github.com/lingbib/lingbib.git")
#         print(out)

def set_remote_upstream_url():
    if config.remote_upstream_url_is_set():
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
    



def test():
    check_all()


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name
