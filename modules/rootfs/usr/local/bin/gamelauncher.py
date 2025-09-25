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

        self.app_id: str = ""
        self.refresh_rate: int = 0
        self.fullscreen_mode: bool = False
        self.always_grab_cursor: bool = True

        self.gamescope_path: str = str(shutil.which("gamescope"))
        self.mangoapp_path: str = str(shutil.which("mangoapp"))
        self.mangohud_path: str = str(shutil.which("mangohud"))
        self.gamemoderun_path: str = str(shutil.which("gamemoderun"))

        self.is_wayland_available: bool = os.environ.get("XDG_SESSION_TYPE") == "wayland"
        self.is_gamescope_available: bool = bool(shutil.which("gamescope"))
        self.is_mangoapp_available: bool = bool(shutil.which("mangoapp"))
        self.is_mangohud_available: bool = bool(shutil.which("mangohud"))
        self.is_gamemoderun_available: bool = bool(shutil.which("gamemoderun"))
        self.is_mangohud_dlsym_available: bool = subprocess.run(["mangohud", "--dlsym"],
                                                                stdout=subprocess.PIPE,
                                                                stderr=subprocess.PIPE).returncode == 0

        for arg in args:
            if arg == "AppId=255710":
                self.app_id = "255710"
                print("[INFO] found {}!".format(arg))
                break

        self.CURRENT_USER: str = os.getlogin()
        self.CURRENT_PLATFORM: str = sys.platform.lower()

    def set_display_resolution(self, width: int, height: int) -> dict[str, int]:
        """
        Sets the display resolution using gamescope.
        Args:
            width (int): The desired width.
            height (int): The desired height.
        Returns:
            Dictionary containing the width and hight
        """
        display_resolution: dict[str, int] = {}

        if not self.is_gamescope_available:
            print("[WARN] gamescope is not available on this system.")

        display_resolution["width"] = width
        display_resolution["height"] = height

        return display_resolution

    def set_refresh_rate(self, new_refresh_rate: int) -> None:
        """
        Set the refresh rate to be used by gamescope.
        Args:
            refresh_rate: int
        """
        self.refresh_rate = new_refresh_rate

    def run(self) -> int:
        """
        Run the game with the specified arguments.
        Returns:
            int: The exit code of the game process.
        """
        if not self.CURRENT_PLATFORM == "linux":
            raise RuntimeError(f"Your platform '{self.CURRENT_PLATFORM}' is not supported.")

        if self.CURRENT_USER == "root":
            raise PermissionError("Do not run this script as root.")

        try:
            display = self.set_display_resolution(1920, 1080)
        except Exception as e:
            raise e

        try:
            self.set_refresh_rate(75)
        except Exception as e:
            raise e

        command_line: list[str] = []

        if self.is_gamescope_available:
            command_line.extend([
                self.gamescope_path,
                "-W", str(display['width']),
                "-H", str(display['height'])
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
            if self.is_mangohud_dlsym_available and \
               self.app_id == "255710":
                command_line.append("--dlsym")

        if self.is_gamemoderun_available:
            command_line.append(self.gamemoderun_path)

        command_line.extend(self.args)

        print("Gamescope is available:", self.is_gamescope_available)
        print("MangoHud is available:", self.is_mangohud_available)
        print("MangoApp is available:", self.is_mangoapp_available)
        print("gamemoderun is available:", self.is_gamemoderun_available)
        print("Wayland is available:", self.is_wayland_available)
        print("MangoHud dlsym enabled:", self.is_mangohud_dlsym_available)
        print("Always grab cursor:", self.always_grab_cursor)
        print("Launch in fullscreen:", self.fullscreen_mode)
        print("Platform:", self.CURRENT_PLATFORM)
        print("Refresh rate:", self.refresh_rate)
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
