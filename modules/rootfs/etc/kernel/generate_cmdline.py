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

CURRENT_PLATFORM: str = sys.platform.lower()
CURRENT_USER: str = getpass.getuser()
CMDLINE_FILE: str = "/etc/kernel/cmdline"

CURRENT_DIR: str = os.getcwd()

def _generate_cmdline(partition: str) -> str:
    """
    Generate the kernel command line for the current system.
    """
    assert partition == "", "A root partition is required."

    args: list[str] = ["blkid", "-s", "PARTUUID", "-o", "value", partition]

    partition_partuuid: str = subprocess.run(args,
                                             capture_output=True,
                                             check=False,
                                             text=True).stdout.strip()

    cmdline_path: str = os.path.join(CURRENT_DIR, "cmdline")

    with open(cmdline_path, "r", encoding="UTF-8") as file:
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
            shutil.copyfile(CMDLINE_FILE, CMDLINE_FILE + ".backup")
        except Exception as e:
            raise e

    with open("/etc/kernel/cmdline", "w", encoding="UTF-8") as item:
        item.write(file)

if __name__ == "__main__":
    assert CURRENT_PLATFORM == "linux", "This script only runs on Linux"
    assert CURRENT_USER == "root", "This script must be run as root"

    root_partition: str = str(input("Enter the root partition (e.g., /dev/sda1): ")).strip()
    cmdline: str = ""

    try:
        cmdline = _generate_cmdline(root_partition)
    except Exception as e:
        raise e
    finally:
        _write_cmdline(cmdline)
