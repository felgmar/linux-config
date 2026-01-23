#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from typing import Any

class GameLauncher():
    """
    A class for optimizing the launching of games
    with the use of tools like gamescope, mangohud and gamemode.
    """
    def __init__(self, args: list[str]) -> None:
        self.args: list[str] = args

        self.app_id: str = ""
        self.resolution: dict[str, int] = {
            "width": -1,
            "height": -1
        }
        self.refresh_rate: int = -1
        self.fullscreen_mode: bool = False
        self.always_grab_cursor: bool = True

        self.gamescope_path: str = str(shutil.which("gamescope"))
        self.mangohud_path: str = str(shutil.which("mangohud"))
        self.mangoapp_path: str = str(shutil.which("mangoapp"))
        self.gamemoderun_path: str = str(shutil.which("gamemoderun"))
        self.is_wayland_available: bool = os.environ.get("XDG_SESSION_TYPE") == "wayland"
        self.is_gamescope_available: bool = bool(shutil.which("gamescope"))
        self.is_mangohud_available: bool = bool(shutil.which("mangohud"))
        self.is_mangoapp_available: bool = bool(shutil.which("mangoapp"))
        self.is_gamemoderun_available: bool = bool(shutil.which("gamemoderun"))
        self.is_mangohud_dlsym_available: bool = False

        if self.is_mangohud_available:
            self.is_mangohud_dlsym_available = True if \
                    subprocess.run([self.mangohud_path, "--dlsym"],
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE).returncode == 0 \
                else False

        for arg in args:
            if arg == "AppId=255710":
                self.app_id = "255710"
                print("[INFO] found {}!".format(arg))
                break

        self.CURRENT_USER: str = os.getlogin()
        self.CURRENT_PLATFORM: str = sys.platform.lower()

    def set_display_resolution(self, width: int, height: int) -> None:
        """
        Set the resolution to be used inside gamescope.
        Args:
            width (int): The desired width.
            height (int): The desired height.
        """
        self.resolution["width"] = width
        self.resolution["height"] = height

    def set_refresh_rate(self, new_refresh_rate: int) -> None:
        """
        Set the refresh rate to be used inside gamescope.
        Args:
            refresh_rate: int
        """
        self.refresh_rate = new_refresh_rate

    def __build_cmdline(self, refresh_rate: int = 60,
                        resolution_width: int = 1920,
                        resolution_height: int = 1080) -> list[str]:
        command_line: list[str] = []

        self.set_refresh_rate(refresh_rate)
        self.set_display_resolution(resolution_width,
                                    resolution_height)

        if self.is_gamescope_available:
            command_line.append(self.gamescope_path)
            command_line.extend([
                "-W", str(self.resolution['width']),
                "-H", str(self.resolution['height'])
                ])
            if not self.refresh_rate == 0:
                command_line.extend(["-r", str(self.refresh_rate)])
            if self.is_wayland_available:
                command_line.append("--expose-wayland")
            if self.fullscreen_mode:
                command_line.append("--fullscreen")
            if self.is_mangohud_available and self.is_mangoapp_available:
                command_line.append("--mangoapp")
            if self.fullscreen_mode:
                command_line.append("--fullscreen")
            if self.always_grab_cursor:
                command_line.append("--force-grab-cursor")
            command_line.append("--")
        else:
            if self.is_mangohud_available:
                command_line.append(self.mangohud_path)
                if self.is_mangohud_dlsym_available and self.app_id == "255710":
                    command_line.append("--dlsym")

        if self.is_gamemoderun_available:
            command_line.append(self.gamemoderun_path)

        command_line.extend(self.args)

        return command_line

    def __prepare(self) -> list[str]:
        """
        Prepare the command line for launching the game.
        Args:
        Raises:
            RuntimeError: If the platform is not supported.
            PermissionError: If the script is run as root.
        """
        if not self.CURRENT_PLATFORM == "linux":
            raise RuntimeError(f"Your platform '{self.CURRENT_PLATFORM}' is not supported.")

        if self.CURRENT_USER == "root":
            raise PermissionError("Do not run this script as root.")

        user_overrides: dict[str, int] = {
            "refresh_rate": -1,
            "resolution_width": -1,
            "resolution_height": -1
        }

        user_overrides["refresh_rate"] = 200
        user_overrides["resolution_width"] = 2560
        user_overrides["resolution_height"] = 1440

        try:
            return self.__build_cmdline(user_overrides["refresh_rate"],
                                        user_overrides["resolution_width"],
                                        user_overrides["resolution_height"])
        except Exception as e:
            raise e

    def run(self, show_debug_info: bool = False) -> int:
        """
        Run the game with the specified arguments.
        Returns:
            int: The exit code of the game process.
        """
        cmdline: list[str] = []
        exit_code: int = 0

        try:
            cmdline = self.__prepare()
        except Exception as e:
            print("An error occurred:", e)

        if show_debug_info:
            debug_info: dict[str, Any] = {
                "args": self.args,
                "app_id": self.app_id,
                "resolution": "{}x{}".format(self.resolution["width"],
                                             self.resolution["height"]),
                "refresh_rate": self.refresh_rate,
                "fullscreen_mode": self.fullscreen_mode,
                "always_grab_cursor": self.always_grab_cursor,
                "is_wayland_available": self.is_wayland_available,
                "is_gamescope_available": self.is_gamescope_available,
                "is_mangohud_available": self.is_mangohud_available,
                "is_mangoapp_available": self.is_mangoapp_available,
                "is_gamemoderun_available": self.is_gamemoderun_available,
                "is_mangohud_dlsym_available": self.is_mangohud_dlsym_available
            }
            for key, value in debug_info.items():
                print(key, value)

        print(f"Running command: {' '.join(cmdline)}")

        try:
            process = subprocess.run(
                cmdline,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            exit_code: int = process.returncode
            process.check_returncode()
        except Exception as e:
            raise e

        return exit_code

if __name__ == "__main__":
    if len(sys.argv[1:]) == 0:
        raise ValueError("No program was specified.")

    try:
        launcher = GameLauncher(sys.argv[1:])
        launcher.run(show_debug_info=True)
    except Exception as e:
        raise e
