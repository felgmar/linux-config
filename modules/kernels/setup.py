#!/usr/bin/env python3
from os import getcwd, chdir, curdir, path, environ
from subprocess import run

class KernelInstaller():
    def __init__(self):
        self.current_dir = getcwd()
        self.kernels_directory = self.current_dir + "/modules/kernels/"
        self.repo_url = ""

    def clone_repo(self, repo_url, repo_directory) -> None:
        previous_dir = curdir
        command = f"git clone {repo_url}"

        try:
            if not path.isdir(self.kernels_directory + repo_directory):
                chdir(self.kernels_directory)
                run(command, shell=True)
                chdir(previous_dir)
            else:
                chdir(self.kernels_directory)
                self.update_repo(repo_directory)
                chdir(previous_dir)
        except Exception:
            raise

    def update_repo(self, repo_directory) -> None:
        previous_dir = curdir
        command = f"git pull"

        try:
            chdir(self.kernels_directory + repo_directory)
            run(command, shell=True)
            chdir(previous_dir)

        except Exception:
            raise

    def install_kernel(self, repo_directory: str, distro: str) -> None:
        if not distro:
            raise ValueError("No distro was specified.")

        previous_dir = curdir

        match distro:
            case "Arch Linux":
                try:
                    self.clone_repo(self.repo_url, repo_directory)
                except Exception:
                    raise

                if path.isfile("customization.cfg"):
                    try:
                        if environ.get("EDITOR"):
                            run("$EDITOR customization.cfg", shell=True)
                    except Exception:
                        raise

                if path.isfile("PKGBUILD"):
                    run("makepkg -si", shell=True)

                    chdir(previous_dir)
                else:
                    self.update_repo(repo_directory)

                    if environ.get("EDITOR"):
                        run("$EDITOR customization.cfg", shell=True)
                    else:
                        raise FileNotFoundError("Could not find a valid text editor")

                    if path.isfile("PKGBUILD"):
                        run("makepkg -sif", shell=True)

                    chdir(previous_dir)
            case _:
                raise NotImplementedError(f"{distro} is not implemented yet")
