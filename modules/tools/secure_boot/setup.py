#!/usr/bin/env python3

from getpass import getuser
from subprocess import run
from modules.packages.setup import PackageManager

class SecureBootManager():
    def install_dependencies(self, dependencies: str, package_manager: str, verbose=False):
        pm = PackageManager()

        current_user = getuser()

        if package_manager != "paru" or "yay":
            for pm_override in "yay", "paru":
                if pm_override == "paru" or "yay":
                    package_manager = pm_override

            if verbose:
                if package_manager != pm_override:
                    print(f"[!] The package manager has been overriden to: {pm_override}")

        dependency_list = []

        for i in dependencies:
            dependency_list.append(i)

        pm.install_packages(dependency_list, package_manager, current_user)

    def backup_boot_files(self, verbose=False) -> None:
        current_user = getuser()
 
        boot_files = [
            "/boot/EFI/BOOT/BOOTX64.EFI",
        ]

        for file in boot_files:
            try:
                match file:
                    case "/boot/EFI/BOOT/BOOTX64.EFI":
                        try:
                            if verbose:
                                if current_user == "root":
                                    run(f"cp -v {file} {file}.backup",
                                                 shell=True, universal_newlines=True, text=True)
                                else:
                                    run(f"sudo cp -v {file} {file}.backup",
                                                 shell=True, universal_newlines=True, text=True)
                            else:
                                if current_user == "root":
                                    run(f"cp {file} {file}.backup",
                                                 shell=True, universal_newlines=True, text=True)
                                else:
                                    run(f"sudo cp {file} {file}.backup",
                                                 shell=True, universal_newlines=True, text=True)
                        except Exception:
                            raise
            except Exception:
                raise

    def install_shim(self, current_user, verbose: bool = False):
        try:
            preloader_files = [
                "/usr/share/preloader-signed/HashTool.efi",
                "/usr/share/preloader-signed/PreLoader.efi",
            ]

            if current_user != "root":
                for file in preloader_files:
                    #if not access(file, R_OK):
                    #    raise PermissionError(f"The file {file} is not accessible.")
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                run(f"sudo cp -v {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                run(f"sudo cp {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            continue
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                run(f"sudo cp -v {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                run(f"sudo cp {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            break

                is_installed = run("sudo bootctl is-installed",
                                   shell=True, universal_newlines=True, capture_output=True, text=True)

                if is_installed.stdout.replace("\n", "") == "yes":
                    if verbose:
                        print(f"[*] systemd-boot is already installed")
                        run("sudo bootctl update",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        run("sudo bootctl update",
                            shell=True, universal_newlines=True, text=True)
                elif is_installed.stdout.replace("\n", "") == "no":
                    if verbose:
                        print(f"[!] systemd-boot is not installed")
                        run("sudo bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
                    else:
                        run("sudo bootctl install --no-variables",
                            shell=True, universal_newlines=True, text=True)
            else:
                for file in preloader_files:
                    #if not access(file, R_OK) or access(file, W_OK):
                    #    raise PermissionError(f"The file {file} is not accessible.")
                    match file:
                        case "/usr/share/preloader-signed/HashTool.efi":
                            if verbose:
                                run(f"cp -v {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                run(f"cp {file} /boot/EFI/BOOT",
                                    shell=True, universal_newlines=True, text=True)
                        case "/usr/share/preloader-signed/PreLoader.efi":
                            if verbose:
                                run(f"cp -v {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)
                            else:
                                run(f"cp {file} /boot/EFI/BOOT/BOOTX64.EFI",
                                    shell=True, universal_newlines=True, text=True)

                is_installed = run("bootctl is-installed",
                                   shell=True, universal_newlines=True,
                                   capture_output=True, text=True)

                if is_installed.stdout.replace("\n", "") == "yes":
                    if verbose:
                        print("[*] systemd-boot is installed")
                        run("bootctl update",
                                   shell=True, universal_newlines=True, text=True)
                    else:
                        run("bootctl update",
                                   shell=True, universal_newlines=True, text=True)
                elif is_installed.stdout.replace("\n", "") == "no":
                    if verbose:
                        print("[!] systemd-boot is not installed")
                        run("bootctl install --no-variables",
                                   shell=True, universal_newlines=True, text=True)
                    else:
                        run("bootctl install --no-variables",
                                   shell=True, universal_newlines=True, text=True)
        except Exception:
            raise
