#!/usr/bin/env python

"""
Usage:
  lingbib.py <command> [<args>...]
  lingbib.py --help
  lingbib.py --version

Use this script to fetch updates from lingbib, merge them with your personal
database, make contributions to the master database, and sync your
personal database with a remote repository. Most commands are simple wrappers
for common git commands used to manage your respositories.

Commands:
  # main commands
  branch  Switch between normal (master) and contributor (contrib) branches.
  config  Check configuration, and attempt to fix any problems.
  pull    Fetch updates from lingbib (upstream) or personal remote
            repo (origin).
  push    Update personal remote repo (origin) with changes to local repo.
  update  Update local repo from lingbib AND personal remote repo if
            applicable, then merge changes to lingbib-master.bib into
            lingbib-personal.bib.
  
  # contrib branch only
  addentry  Process new entry, integrate into local master database,
              stage, and commit.

Options:
  -h --help  Show this help text.
  --version  Show version.

See 'lingbib.py help <command>' for more information on a specific command.
For futher help, see README.md or https://github.com/lingbib/lingbib.
"""


from __future__ import print_function
import sys

from lib.docopt import docopt

from util import *
import addentry
import config
import update


__author__ =  "Kenneth Hanson"
__version__ = "0.0.0"
__date__ =    "6/27/2015"


# mapping from command names to main function from each subscript
COMMANDS = {'addentry':addentry.addentry,
            'config':config.config,
            'update':update.update}


def main(argv):
    """
    Interpret command line arguments and run the corresponding command.
    """
    args = docopt(__doc__, argv=argv, version=__version__,
                  help=True, options_first=True)
    
    cmd = args['<command>']
    subargv = [cmd] + args['<args>']
    
    if cmd in COMMANDS:
        handler = COMMANDS[cmd]
        handler(subargv)
    elif cmd == 'help':
        help_text(subargv)
    elif cmd == 'version':
        version_text(subargv)
    else:
        raise InputError("Invalid command: {cmd}".format(cmd=cmd) +
                        " Check that the 'usage' string and the COMMANDS" +
                        " dictionary are in sync.")


def help_text(argv):
    """
    Given a lingbib command, print help text that command.
    If none give, print the main help text.
    In either case, the docopt implementation of the '--help' option is used.
    """
    if len(argv) > 1 and argv[1] in COMMANDS:
        cmd = argv[1]
        handler = COMMANDS[cmd]
        handler(['--help'])
    else:
        main(['--help'])


def version_text(argv):
    """
    Print the program version.
    Uses the docopt implementation of the '--version' option.
    """
    main(['--version'])


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name