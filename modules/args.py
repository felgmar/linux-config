#/usr/bin/env python3

"""
This module is responsible for handling the ArgumentParser class.
"""

import argparse

class ArgumentParser:
    """
    This class manages the command line arguments.
    """
    def __init__(self):
        self.actions: list[str] = [
            "setup-secure-boot", "install-tkg-kernel",
            "install-packages", "setup-rootfs", "setup-services"
        ]

        self.parser = argparse.ArgumentParser(prog="linux-config")
        self.group = self.parser.add_mutually_exclusive_group()

    def populate_args(self):
        """
        This method populates the ArgumentParser object with the necessary arguments.
        """
        self.parser.add_argument("-a", "--action", choices=self.actions, type=str,
                            help="Runs the specified script. Available options are " +
                            ", ".join(self.actions), metavar="")

        self.parser.add_argument("-v", "--verbose", action="store_true", help="Print more messages")
        self.group.add_argument("--version", action="version", version="%(prog)s 1.0")

    def parse_args(self):
        """
        This method parses the command line arguments.
        """
        return self.parser.parse_args()
