#!/usr/bin/env python3

from operator import is_
import shutil
import subprocess
import sys
import argparse

args = argparse.ArgumentParser(
    description="Launch a game with gamemoderun and mangohud.",
    epilog="This script requires gamemoderun and mangohud to be installed on your system.",
    prog="gamelauncher.py"
)

args.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
args.add_argument("--dlsym", action="store_true", help="Enable dlsym for mangohud.", default=False)
args.add_argument("game", nargs="*", help="The game to run. Provide the command and its arguments.")
args.add_argument(
    "--version",
    action="version",
    version="%(prog)s 0.1",
    help="Show the version of the gamelauncher script."
)
parser = args.parse_args()

is_gamescope_available: bool = shutil.which("gamescope") is not None
is_mangohud_available: bool = shutil.which("mangohud") is not None
is_gamemoderun_available: bool = shutil.which("gamemoderun") is not None
is_dlsym_enabled: bool = parser.dlsym

def __run_game(verbose: bool = False) -> int:
    """
    Run the game with gamemoderun and mangohud.
    """
    exit_code: int = -1
    game = sys.argv[1:]
    command: list[str] = ["gamemoderun", "mangohud"] + game

    if verbose:
        print("[VERBOSE] Running command: {}".format(" ".join(command)))

    if not game:
        raise ValueError("No game specified to run.")

    try:
        process = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False
        )
        exit_code = process.returncode
    except Exception as e:
        raise e
    finally:
        return exit_code

if __name__ == "__main__":
    try:
        exit_code = __run_game(verbose=True)
        sys.exit(exit_code)
    except ValueError as e:
        raise e
