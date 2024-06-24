#!/usr/bin/env python3
import os, getpass, subprocess

class KernelInstaller():
    def __init__(self):
        current_distro_cmd: subprocess.CompletedProcess[str] = subprocess.run("lsb_release -ds", shell=True, universal_newlines=True, capture_output=True, text=True)
        self.current_distro = current_distro_cmd.stdout.replace("\"", "").removesuffix("\n")
        self.current_dir: str = os.getcwd()
        self.kernels_directory: str = self.current_dir + "/modules/kernels/"
        self.repo_url: str = ""
        self.current_user: str = getpass.getuser()

    def clone_repo(self, repo_url, repo_directory) -> None:
        previous_dir: str = os.curdir
        command: str = f"git clone {repo_url}"

        try:
            if not os.path.isdir(self.kernels_directory + repo_directory):
                os.chdir(self.kernels_directory)
                subprocess.run(command, shell=True)
                os.chdir(previous_dir)
            else:
                os.chdir(self.kernels_directory)
                self.update_repo(repo_directory)
                os.chdir(previous_dir)
        except Exception:
            raise

    def update_repo(self, repo_directory) -> None:
        previous_dir: str = os.curdir
        command: str = f"git pull"

        try:
            os.chdir(self.kernels_directory + repo_directory)
            subprocess.run(command, shell=True)
            os.chdir(previous_dir)

        except Exception:
            raise

    def install_kernel(self, repo_directory: str, verbose: bool = False) -> None:
        if not self.current_distro:
            raise ValueError("No distro was specified.")

        previous_dir: str = os.curdir

        match self.current_distro:
            case "Arch Linux":
                try:
                    self.clone_repo(self.repo_url, repo_directory)
                except Exception:
                    raise

                if os.path.isfile("customization.cfg"):
                    try:
                        if os.environ.get("EDITOR"):
                            subprocess.run("$EDITOR customization.cfg", shell=True)
                        else:
                            print("Could not find a valid text editor.")
                            user_text_editor: str = str(input("Specify an alternate text editor: "))

                            if user_text_editor:
                                print(f"The text editor has been set manually to: {user_text_editor}")

                            subprocess.run(f"{user_text_editor} customization.cfg", shell=True)
                    except Exception:
                        raise

                if os.path.isfile("PKGBUILD"):
                    subprocess.run("makepkg -si", shell=True)

                    os.chdir(previous_dir)
                else:
                    self.update_repo(repo_directory)

                    if os.path.isfile("customization.cfg"):
                        try:
                            if os.environ.get("EDITOR"):
                                subprocess.run("$EDITOR customization.cfg", shell=True)
                            else:
                                print("You do not seem to have set a default text editor.")
                                user_text_editor: str = str(input("Specify an alternate text editor: "))

                            if user_text_editor:
                                if verbose:
                                    print(f"The text editor has been set manually to: {user_text_editor}")

                                subprocess.run(f"{user_text_editor} customization.cfg", shell=True)
                            else:
                                if verbose:
                                    print("No text editor was specified, omitting customization.")
                        except Exception:
                            raise

                    if os.path.isfile("PKGBUILD"):
                        subprocess.run("makepkg -sif", shell=True)

                    os.chdir(previous_dir)
            case _:
                if self.current_distro:
                    raise NotImplementedError(self.current_distro + " is not implemented yet")
                else:
                    raise ValueError("No distribution was specified.")
