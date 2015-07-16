"""
Utility functions for lingbib app.

Logging functions currently use the print function. In the future, they will
use the Python logging system.
"""

def debug(obj):
    print("DEBUG: " + str(obj))

def info(msg):
    print("INFO: " + msg)

def warning(msg):
    print("WARNING: " + msg)

def error(msg):
    print("ERROR: " + msg)