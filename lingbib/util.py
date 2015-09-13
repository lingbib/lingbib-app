"""
Utility functions for lingbib app.

Logging functions currently use the print function. In the future, they will
use the Python logging system.
"""

from __future__ import print_function
import textwrap

def debug(msg):
    _wrapprint("DEBUG: " + msg)

def debug_obj(obj):
    _wrapprint("DEBUG: " + str(obj))

def info(msg):
    _wrapprint("INFO: " + msg)

def warning(msg):
    _wrapprint("WARNING: " + msg)

def error(msg):
    _wrapprint("ERROR: " + msg)

def gitout(msg):
    """Print without added trailing newline. Used for output from calls to Git."""
    _wrapprint("GIT: " + msg.strip())

def _wrapprint(s):
    """Wrap text to proper terminal width, with slight hanging indentation."""
    print(textwrap.fill(s, width=80, subsequent_indent='  '))