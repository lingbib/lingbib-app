#!/usr/bin/env python

"""
lingbib.py

This script provides a simple command line interface for using and contributing
to lingbib.
"""


from __future__ import print_function
import sys
from subprocess import call

from lib.docopt import docopt


__author__ =  "Kenneth Hanson"
__version__ = "0.0.0"
__date__ =    "6/27/2015"


usage = """
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


def debug(obj):
    print("DEBUG: " + str(obj))


#
# Main function
#

"""
Interpret command line arguments and run the corresponding command.
"""
def main(argv):
    args = docopt(usage, argv=argv, version=__version__,
                  help=True, options_first=True)
    
    cmd = args['<command>']
    subargv = [cmd] + args['<args>']

    if cmd in COMMANDS:
        action = COMMANDS[cmd]
        action(subargv)
    else:
        raise Exception("Invalid command: {cmd}".format(cmd=cmd) +
                        " Check that the 'usage' string and the COMMANDS" +
                        " dictionary are in sync.")


#
# Command definitions
#
# All functions expect a list containing the command name followed by any
#   options and arguments.
#


def add_entry(argv):
    """
    Usage:
      lingbib.py addentry [options] FILE
      lingbib.py addentry [options] (-i | --interactive)
      lingbib.py --help

    Arguments:
      FILE  File containing new entries to process.
      
    Options:
      -i --interactive  Opens the default editor for quick data entry,
                          on systems where this feature exists.
      -h --help         Show this help text and quit.
    """
    args = docopt(add_entry.__doc__, argv=argv,help=True)

    # print(args)

    if args['FILE']:
        # run script in debug mode
        print("Calling scripts/addentry.sh with '{}'".format(args['FILE']))
        # call(['sh', '-n', 'scripts/addentry.sh', args['FILE']])
        raise NotImplementedError('Shell script not yet integrated.') 
    elif args['--interactive']:
        raise NotImplementedError('Interactive mode not yet implemented.')
    else:
        # TODO: remove after testing code
        raise Exception("Reached the end of command line arg processing"
                        "without doing anything. Code has a logic error.")



def help_msg(argv):
    """
    Given a lingbib command, print help text that command.
    If none give, print the main help text.
    In either case, the docopt implementation of the '--help' option is used.
    """
    if len(argv) > 1 and argv[1] in COMMANDS:
        cmd = argv[1]
        action = COMMANDS[cmd]
        action(['--help'])
    else:
        main(['--help'])



def update(argv):
    """
    Usage:
      lingbib.py update [options] [PERSONAL_DB]
      lingbib.py update --help

    Arguments:
      PERSONAL_DB  Path to personal database. [default: lingbib-personal.bib]
      
    Options:
      -h --help         Show this help text and quit.
    """
    args = docopt(update.__doc__, argv=argv, help=True)

    # print(args)

    db = args['PERSONAL_DB']
    if db == None:
        db = "lingbib-personal.bib"

    # run script in debug mode
    # call(['sh', '-n', 'scripts/update_personal_db.sh', db])
    print("Calling scripts/update_personal_db.sh with '{}'".format(db))
    raise NotImplementedError('Shell script not yet integrated.') 


def version(argv):
    """
    Print the program version.
    Uses the docopt implementation of the '--version' option.
    """
    main(['--version'])


COMMANDS = {'addentry':add_entry,
            'update':update,
            'help':help_msg,
            'version':version}


if __name__ == '__main__':
    main(sys.argv[1:]) # strip program name