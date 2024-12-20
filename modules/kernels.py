#!/usr/bin/env python3

"""
Module containing the KernelManager class.
"""

import os
import getpass
import subprocess

from modules.repository import RepositoryManager

class KernelManager():
    """
    Manages the installation of custom kernels.
    """
    def __init__(self):
        self.current_distro_cmd: subprocess.CompletedProcess[str] = \
            subprocess.run("lsb_release -ds", shell=True, universal_newlines=True,
                           capture_output=True, check=True, text=True)

        self.current_user: str = getpass.getuser()
        self.current_distro: str = self.current_distro_cmd.stdout
        self.readable_current_distro = self.current_distro.replace("\"", "").removesuffix("\n")

        self.current_dir: str = os.getcwd()

    def clone_kernel(self) -> None:
        """
        Clones the custom kernel repository.
        """
        rm = RepositoryManager()
        try:
            rm.clone_repo()
        except Exception as e:
            raise e

    def install_kernel(self, verbose: bool = False) -> None:
        """
        Installs a custom kernel.
        """
        previous_dir: str = self.current_dir

        rm = RepositoryManager()
        rm.repo_url = "https://github.com/frogging-family/linux-tkg.git"
        rm.repo_dir = "linux-tkg"

        if not self.current_distro:
            raise ValueError("No distro was specified.")

        match self.current_distro:
            case "Arch Linux":
                try:
                    self.clone_kernel()
                except Exception as e:
                    raise e

                if not os.path.exists(os.path.join(rm.repositories_dir, rm.repo_dir)):
                    raise IOError(os.path.join(rm.repositories_dir, rm.repo_dir),
                                  ": directory not found")

                if not os.path.isfile(os.path.join(rm.repositories_dir, rm.repo_dir,
                                                   "customization.cfg")):
                    raise FileNotFoundError("customization.cfg: file not found")

                try:
                    os.chdir(os.path.join(rm.repositories_dir, rm.repo_dir))
                except Exception as e:
                    raise e

                if os.environ.get("EDITOR"):
                    subprocess.run("$EDITOR customization.cfg", shell=True, check=True)
                else:
                    print("You do not seem to have set a default text editor.\n" + \
                          "to edit the customization.cfg file.")
                    try:
                        user_text_editor: str = input("Specify an alternate text editor: ")
                    except EOFError as e:
                        raise e

                    if user_text_editor:
                        if verbose:
                            print(f"The text editor has been set manually to: {user_text_editor}")

                        subprocess.run(f"{user_text_editor} customization.cfg",
                                       shell=True, check=True)
                    else:
                        if verbose:
                            print("No text editor was specified, omitting customization.")

                if os.path.isfile("PKGBUILD"):
                    subprocess.run("makepkg -sirf", shell=True, check=True)

                    os.chdir(previous_dir)
            case _:
                raise NotImplementedError(self.current_distro + " is not implemented yet.")
