#!/usr/bin/env python3

"""
Module containing the KernelManager class.
"""

import os
import getpass
import shutil
import subprocess

from modules.repository import RepositoryManager

class KernelManager():
    """
    Manages the installation of custom kernels.
    """
    def __init__(self, kernel_url: str, kernel_dir: str):
        self.CURRENT_USER: str = getpass.getuser()
        self.CURRENT_DIR: str = os.getcwd()
        self.KERNEL_URL: str = kernel_url
        self.KERNEL_DIR: str = kernel_dir
        self.repo_manager: RepositoryManager = \
            RepositoryManager(repo_url=self.KERNEL_URL,
                              repo_dir=self.KERNEL_DIR)

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
        PREVIOUS_DIR: str = self.CURRENT_DIR
        FULL_REPOSITORY_PATH: str = os.path.join(self.repo_manager.repositories_dir,
                                                 self.repo_manager.repo_dir)
        DEFAULT_TEXT_EDITOR: str | None = os.environ.get("EDITOR")
        CUSTOM_DEFINED_TEXT_EDITOR: str | None = shutil.which("nano") or \
                                                 shutil.which("vim") or \
                                                 shutil.which("vi")
        
        assert os.path.isdir(FULL_REPOSITORY_PATH), f"Could not find the repository directory."

        if not os.path.isdir(FULL_REPOSITORY_PATH):
            try:
                self.clone_kernel()
            except Exception as e:
                raise e
        else:
            try:
                self.update_kernel()
            except Exception as e:
                raise e

        os.chdir(FULL_REPOSITORY_PATH)

        assert os.path.isfile ("customization.cfg"), "customization.cfg file is missing."
        assert os.path.isfile ("PKGBUILD"), "PKGBUILD file is missing."

        if CUSTOM_DEFINED_TEXT_EDITOR:
            if verbose:
                print(f"The text editor has been manually set to: {CUSTOM_DEFINED_TEXT_EDITOR}")
            try:
                subprocess.run([CUSTOM_DEFINED_TEXT_EDITOR, "customization.cfg"], check=True)
            except subprocess.CalledProcessError as e:
                raise e
        elif DEFAULT_TEXT_EDITOR:
            if verbose:
                print(f"The text editor has been set to: {DEFAULT_TEXT_EDITOR}")
            try:
                subprocess.run([DEFAULT_TEXT_EDITOR, "customization.cfg"], check=True)
            except subprocess.CalledProcessError as e:
                raise e
        else:
            raise EnvironmentError("No valid text editor was found.")

        subprocess.run(["makepkg", "-sirf"], check=True)

        os.chdir(PREVIOUS_DIR)
