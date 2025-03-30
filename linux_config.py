#!/usr/bin/env python3

"""
Main file for the Linux configuration script.
"""

from lib.event_handler import parse_actions

if __name__ == "__main__":
    try:
        parse_actions()
    except Exception as e:
        raise e
