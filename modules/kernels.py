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
    def __init__(self, kernel_url: str, kernel_dir: str):
        self.current_distro_cmd: subprocess.CompletedProcess[str] = \
            subprocess.run("lsb_release -ds", shell=True, universal_newlines=True,
                           capture_output=True, check=True, text=True)

        self.current_user: str = getpass.getuser()
        self.current_distro: str = \
            self.current_distro_cmd.stdout.replace("\"", "").removesuffix("\n")

        self.current_dir: str = os.getcwd()

        self.kernel_url: str = kernel_url
        self.kernel_dir: str = kernel_dir

        self.repo_manager: RepositoryManager = RepositoryManager(repo_url=self.kernel_url,
                                                                 repo_dir=self.kernel_dir)

    def clone_kernel(self) -> None:
        """
        Clones the custom kernel repository.
        """
        try:
            self.repo_manager.clone_repo()
        except Exception as e:
            raise e
    
    def update_kernel(self) -> None:
        """
        Updates the custom kernel repository.
        """
        try:
            self.repo_manager.update_repo()
        except Exception as e:
            raise e

    def install_kernel(self, verbose: bool = False) -> None:
        """
        Installs a custom kernel.
        """
        previous_dir: str = self.current_dir

        if not self.current_distro:
            raise ValueError("No distro was specified.")

        match self.current_distro:
            case "Arch Linux":
                if not os.path.isdir(os.path.join(self.repo_manager.repositories_dir,
                                                  self.repo_manager.repo_dir)):
                    try:
                        self.clone_kernel()
                    except Exception as e:
                        raise e
                else:
                    try:
                        self.update_kernel()
                    except Exception as e:
                        raise e
                
                os.chdir(os.path.join(self.repo_manager.repositories_dir, self.repo_manager.repo_dir))

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
