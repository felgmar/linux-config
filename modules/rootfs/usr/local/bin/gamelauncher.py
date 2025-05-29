#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil

class GameLauncher():
    """
    A class for optimizing the launching of games
    with the use of tools like gamescope, mangohud and gamemode.
    """
    def __init__(self, args: list[str]) -> None:
        self.args: list[str] = args
        self.is_gamescope_available: bool = bool(shutil.which("gamescope"))
        self.is_mangohud_available: bool = bool(shutil.which("mangohud"))
        self.is_gamemoderun_available: bool = bool(shutil.which("gamemoderun"))
        self.is_mangohud_dlsym_enabled: bool = False

        for arg in args:
            if arg == "AppId=255710":
                self.is_mangohud_dlsym_enabled = True
                #print("found {}!".format(arg))

        self.gamescope_path: str = str(shutil.which("gamescope"))
        self.mangohud_path: str = str(shutil.which("mangohud"))
        self.gamemoderun_path: str = str(shutil.which("gamemoderun"))

        self.CURRENT_USER: str = os.getlogin()
        self.CURRENT_PLATFORM: str = sys.platform.lower()

    def run(self) -> int:
        """
        Run the game with the specified arguments.
        Returns:
            int: The exit code of the game process.
        """
        if self.CURRENT_PLATFORM != "linux":
            raise RuntimeError("Your platform {} is not compatible.",
                               self.CURRENT_PLATFORM)

        if self.CURRENT_USER == "root":
            raise PermissionError("Do not run this script as root.")

        command_line: list[str] = []

        if self.is_gamescope_available:
            command_line.append(self.gamescope_path)
            command_line.append("--")
        else:
            if self.is_mangohud_available:
                command_line.append(self.mangohud_path)
            if self.is_mangohud_dlsym_enabled:
                command_line.append("--dlsym")
        if self.is_gamemoderun_available:
            command_line.append(self.gamemoderun_path)

        command_line.extend(self.args)
    
        print("gamescope is available:", self.is_gamescope_available)
        print("mangohud is available:", self.is_mangohud_available)
        print("gamemoderun is available:", self.is_gamemoderun_available)
        print("MangoHud dlsym enabled:", self.is_mangohud_dlsym_enabled)
        print("Platform:", self.CURRENT_PLATFORM)
        print("Running as:", self.CURRENT_USER)
        print("Running command:", ' '.join(command_line))

        exit_code: int = 0
        try:
            process = subprocess.run(
                command_line,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True
            )
            exit_code: int = process.returncode
        except Exception as e:
            raise e
        finally:
            return exit_code

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        raise ValueError("No program was specified.")

    try:
        launcher = GameLauncher(sys.argv[1:])
        launcher.run()
    except Exception as e:
        raise e
