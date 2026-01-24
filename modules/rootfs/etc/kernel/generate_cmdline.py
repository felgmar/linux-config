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
from typing import Any

CURRENT_PLATFORM: str = sys.platform.lower()
CURRENT_USER: str = getpass.getuser()
CMDLINE_FILE: str = "/etc/kernel/cmdline"

CURRENT_DIR: str = os.getcwd()


def __get_root_partition_info() -> str:
    args: list[str] = ["findmnt", "-n", "-T", "/", "-o", "PARTUUID"]

    try:
        partition_partuuid: str = subprocess.run(args,
                                                 capture_output=True,
                                                 text=True).stdout.strip()
    except Exception as e:
        raise e

    return partition_partuuid

def __generate_parameters(root_uuid: str | None,
                          rootflags: str = "subvol=@",
                          rootfstype: str = "btrfs") -> dict[str, Any]:
    assert root_uuid is not None, "A root UUID is required."

    return {
        "root_uuid": root_uuid,
        "rootflags": rootflags,
        "rootfstype": rootfstype
    }

def __generate_cmdline() -> str:
    """
    Generate the kernel command line for the current system.
    """
    CMDLINE_FILE_PATH: str = os.path.join(CURRENT_DIR, "cmdline")
    root_partition_info = __get_root_partition_info()

    parameters = __generate_parameters(root_partition_info)

    with open(CMDLINE_FILE_PATH, "r", encoding="UTF-8") as file:
        new_cmdline: str = re.sub(r"<.*>", parameters["root_uuid"], file.read().strip())

    return new_cmdline

def __write_cmdline(file: str) -> None:
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

    cmdline: str = ""

    try:
        cmdline = __generate_cmdline()
    except Exception as e:
        raise e
    finally:
        __write_cmdline(cmdline)
        print(cmdline)
