"""
Utility functions for lingbib app.

Logging functions currently use the print statement. In the future, they will
use the Python logging system.
"""

def debug(obj):
    print("DEBUG: " + str(obj))

def warning(msg):
    print("WARNING: " + msg)