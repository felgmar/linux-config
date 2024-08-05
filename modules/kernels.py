#!/usr/bin/env python3
import os, getpass, subprocess

class kernel_manager():
    def __init__(self):
        self.repo_url: str = ""
        self.repo_dir: str = ""

        self.current_distro_cmd: subprocess.CompletedProcess[str] = \
            subprocess.run("lsb_release -ds", shell=True, universal_newlines=True,
                           capture_output=True, text=True)

        self.current_user: str = getpass.getuser()
        self.current_distro: str = self.current_distro_cmd.stdout.replace("\"", "").removesuffix("\n")

        self.current_dir: str = os.getcwd()
        self.kernels_directory: str = self.current_dir + "/modules/kernels/"

    def update_repo(self) -> None:
        previous_dir: str = os.curdir
        command: str = f"git pull {self.repo_dir}"

        try:
            if os.path.isdir(self.kernels_directory + self.repo_dir):
                os.chdir(self.kernels_directory)
                subprocess.run(command, shell=True)
                os.chdir(previous_dir)
        except:
            raise IOError(f"{self.kernels_directory + self.repo_dir}: such directory does not exist.")

    def clone_repo(self) -> None:
        previous_dir: str = os.curdir
        command: str = f"git clone {self.repo_url} {self.repo_dir}"

        try:
            if not os.path.isdir(self.kernels_directory + self.repo_dir):
                os.chdir(self.kernels_directory)
                subprocess.run(command, shell=True)
                os.chdir(previous_dir)
            else:
                self.update_repo()
        except Exception:
            raise

    def install_kernel(self, verbose: bool = False) -> None:
        previous_dir: str = os.curdir

        if not self.current_distro:
            raise ValueError("No distro was specified.")
        
        try:
            self.clone_repo()
        except:
            raise

        match self.current_distro:
            case "Arch Linux":
                if self.repo_dir == "linux-tkg":
                    os.chdir(self.kernels_directory + self.repo_dir)
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
                        subprocess.run("makepkg -sirf", shell=True)

                        os.chdir(previous_dir)
                    else:
                        raise FileNotFoundError("customization.cfg: file not found")
                else:
                    if os.path.isfile("PKGBUILD"):
                        subprocess.run("makepkg -sirf", shell=True)
                        os.chdir(previous_dir)
            case _:
                if self.current_distro:
                    raise NotImplementedError(self.current_distro + " is not implemented yet.")
                else:
                    raise ValueError("No distribution was specified.")
