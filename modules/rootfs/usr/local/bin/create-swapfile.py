#!/bin/sh

import getpass
import os
import subprocess
import sys

SWAP_FILE_LOCATION: str ="/swapfile"
SWAP_LABEL: str ="swap"
SWAP_FILE_SIZE: int = 32768
SWAPON_ARGS: list[str] = ["--priority", "60"]

IS_SWAP_FILE_PRESENT: bool = os.path.exists(SWAP_FILE_LOCATION)

CREATE_SWAP_FILE_COMMAND: list[str] = ["dd", "if=/dev/zero", f"of={SWAP_FILE_LOCATION}",
                                       "bs=1M", f"count={SWAP_FILE_SIZE}", "conv=fsync",
                                       "status=progress"]
SECURE_SWAP_FILE_COMMAND: list[str] = ["chmod", "0600", SWAP_FILE_LOCATION]
FORMAT_SWAP_FILE_COMMAND: list[str] = ["mkswap", "-L", SWAP_LABEL, SWAP_FILE_LOCATION]
ENABLE_SWAP_FILE_COMMAND: list[str] = ["swapon", *SWAPON_ARGS, SWAP_FILE_LOCATION]

CURRENT_USER: str = getpass.getuser()

if __name__ == "__main__":
    if not CURRENT_USER == "root":
        print("This script must be run as root.")
        sys.exit(1)

    if IS_SWAP_FILE_PRESENT:
        print(f"{SWAP_FILE_LOCATION} already exists, creation skipped.")
        sys.exit(2)

    try:
        print("Creating swap file...")
        process = subprocess.run(CREATE_SWAP_FILE_COMMAND, check=True)
        process.check_returncode()
    except Exception as e:
        print(f"An error occurred while creating the swap file: {e}")
        sys.exit(3)

    try:
        print("Securing swap file...")
        process = subprocess.run(SECURE_SWAP_FILE_COMMAND, check=True)
        process.check_returncode()
    except Exception as e:
        print(f"An error occurred while securing the swap file: {e}")
        sys.exit(4)

    try:
        print("Formatting swap file...")
        process = subprocess.run(FORMAT_SWAP_FILE_COMMAND, check=True)
        process.check_returncode()
    except Exception as e:
        print(f"An error occurred while formatting the swap file: {e}")
        sys.exit(5)

    try:
        print("Enabling swap file...")
        process = subprocess.run(ENABLE_SWAP_FILE_COMMAND, check=True)
        process.check_returncode()
    except Exception as e:
        print(f"An error occurred while enabling the swap file: {e}")
        sys.exit(6)
