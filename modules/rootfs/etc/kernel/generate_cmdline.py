#!/usr/bin/env python3

"""
This module helps with the creation of generating a cmdline for the Linux kernel.
"""

import os
import re
import shutil
import sys
import subprocess
import getpass
import datetime

CURRENT_PLATFORM: str = sys.platform.lower()
CURRENT_USER: str = getpass.getuser()
CMDLINE_FILE: str = "/etc/kernel/cmdline"

CURRENT_DIR: str = os.getcwd()

def _generate_cmdline(directory: str, output_column: str) -> str:
    """
    Generate the kernel command line for the current system.
    """
    assert directory == "", "A root partition is required."

    CMDLINE_FILE_PATH: str = os.path.join(CURRENT_DIR, "cmdline")

    args: list[str] = ["findmnt", "-n", "-T", directory, "-o", output_column]

    try:
        partition_partuuid: str = subprocess.run(args,
                                                 capture_output=True,
                                                 check=False,
                                                 text=True).stdout.strip()
    except Exception as e:
        raise e

    with open(CMDLINE_FILE_PATH, "r", encoding="UTF-8") as file:
        new_cmdline: str = re.sub(r"<.*>", partition_partuuid, file.read().strip())

    return new_cmdline

def _write_cmdline(file: str) -> None:
    """
    Write the generated command line to the kernel command line file.
    """
    assert os.path.exists(CMDLINE_FILE[:-8]), f"The directory {CMDLINE_FILE[:-8]} does not exist"

    assert os.access(CMDLINE_FILE, os.W_OK), f"{CMDLINE_FILE}: cannot write to file"

    if os.path.isfile(CMDLINE_FILE):
        try:
            date: str = "{:%Y%m%d_%H%M%S}".format(datetime.datetime.now())
            shutil.copyfile(CMDLINE_FILE, CMDLINE_FILE + f".backup_{date}")
        except Exception as e:
            raise e

    try:
        with open("/etc/kernel/cmdline", "w", encoding="UTF-8") as item:
            item.write(file)
    except Exception as e:
        raise e

if __name__ == "__main__":
    assert CURRENT_PLATFORM == "linux", "This script only runs on Linux"
    assert CURRENT_USER == "root", "This script must be run as root"

    OUTPUT_COLUMN: str = "PARTUUID"
    ROOT_DIRECTORY: str = "/"

    cmdline: str = ""

    try:
        cmdline = _generate_cmdline(ROOT_DIRECTORY, OUTPUT_COLUMN)
    except Exception as e:
        raise e
    finally:
        _write_cmdline(cmdline)
