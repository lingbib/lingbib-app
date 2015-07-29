"""
Utility functions for lingbib app.

Logging functions currently use the print function. In the future, they will
use the Python logging system.
"""

from __future__ import print_function

def debug(msg):
    print("DEBUG: " + msg)

def debug_obj(obj):
    print("DEBUG: " + str(obj))

def info(msg):
    print("INFO: " + msg)

def warning(msg):
    print("WARNING: " + msg)

def error(msg):
    print("ERROR: " + msg)

def gitout(msg):
    print("GIT: " + msg, end='')