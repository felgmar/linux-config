#!/usr/bin/env python3
import shutil
from struct import pack
from subprocess import run
from xmlrpc.client import Boolean

class PackageManager():
    def __init__(self):
        self.running_distro = run("lsb_release -ds", shell=True,
                                  universal_newlines=True, capture_output=True, text=True)
        self.readable_running_distro = self.running_distro.stdout.replace("\"", "").removesuffix("\n")

    def get_package_manager(self, distro: str, overridePackageManager: Boolean = False) -> str:
        package_managers = [
            "apt",
            "dnf",
            "pacman",
            "zypper"
        ]

        for f in package_managers:
            if shutil.which(f):
                pm_bin = f
                break

        if overridePackageManager:
            if distro == "Arch Linux" or pm_bin == "pacman":
                pm_bin = "paru"

        return pm_bin

    def install_aur_helper(self, distro: str, package_manager: str):
        if distro == "Arch Linux":
            if package_manager != "yay" or package_manager != "paru":
                raise ValueError(f"[!] {package_manager} is not an AUR helper.")
        else:
            raise ValueError(f"[!] {distro}: unsupported distribution.")

    def convert_list_to_str(self, list: list[str]) -> str:
        newlist = ' '.join(list)

        return newlist

    def get_main_packages_list(self, distro: str) -> list[str]:
        if distro == "Arch Linux":
            arch_main = [
                "apparmor",
                "archlinux-wallpaper",
                "bridge-utils",
                "chezmoi",
                "clamtk",
                "curl",
                "dnsmasq",
                "fail2ban",
                "fastfetch",
                "firewalld",
                "fwupd",
                "gamemode",
                "intel-ucode",
                "linux",
                "linux-hardened",
                "linux-hardened-headers",
                "linux-headers",
                "linux-lts",
                "linux-lts-headers",
                "linux-zen",
                "linux-zen-headers",
                "lutris",
                "pacman-contrib",
                "pipewire-alsa",
                "pipewire-pulse",
                "power-profiles-daemon",
                "qemu-desktop",
                "steam",
                "swtpm",
                "virt-manager",
                "wget",
                "xdg-user-dirs",
                "zram-generator",
                "zsh",
                "zsh-autosuggestions",
                "zsh-completions",
                "zsh-syntax-highlighting"
            ]

            return arch_main
        else:
            raise ValueError(f"[!] {distro} is not supported.")

    def get_package_list(self, distro: str, only_get_aur: bool=False) -> list[str]:
        if distro == "Arch Linux":
            aur = [
                "ananicy-git",
                "archlinux-artwork",
                "duckstation-git",
                "mangohud-git",
                "pcsx2-git",
                "plymouth-theme-archlinux",
                "ppsspp-git",
                "preloader-signed",
                "rate-mirrors",
                "rpcs3-git",
                "spotify",
                "steam-devices-git",
                "ventoy-bin",
                "visual-studio-code-bin",
                "zsh-theme-powerlevel10k-git"
            ]

            arch_gnome = [
                "gdm",
                "gnome-backgrounds",
                "gnome-browser-connector",
                "gnome-control-center",
                "gnome-disk-utility",
                "gnome-keyring",
                "gvfs",
                "gvfs-mtp",
                "gvfs-nfs",
                "malcontent",
                "nautilus"
            ]

            arch_kde = [
                "bluedevil",
                "dolphin",
                "gnome-keyring",
                "kdeconnect",
                "kde-gtk-config",
                "kdialog",
                "kscreen",
                "kwalletmanager",
                "kwallet-pam",
                "plasma-desktop",
                "plasma-nm",
                "plasma-pa",
                "plasma-wayland-session",
                "powerdevil"
            ]

            arch_xfce = [
                "xfce4"
            ]

            if only_get_aur:
                selected_pkglist = aur
                return selected_pkglist
            else:
                print("Desktop managers available: arch_gnome, arch_kde, arch_xfce")
        else:
            raise ValueError(f"[!] {distro} is not supported.")

        selected_pkglist = input("Select a list: ")

        while True:
            match selected_pkglist:
                case "aur":
                    raise ValueError("For selected the AUR package list, use only_get_aur=True instead in linux-config.py.")
                case "arch_gnome":
                    selected_pkglist = arch_gnome
                    break
                case "arch_kde" | "arch_plasma":
                    selected_pkglist = arch_kde
                    break
                case "arch_xfce":
                    selected_pkglist = arch_xfce
                    break
                case _:
                    if selected_pkglist != "":
                        raise ValueError(f"{selected_pkglist}: invalid list specified.")
                    else:
                        raise EOFError("no output was detected.")

        return selected_pkglist

    def install_packages(self, pkglist: list[str], package_manager: str, current_user: str) -> None:
        if pkglist == "":
            user_packages = self.convert_list_to_str(pkglist)
            main_packages = self.convert_list_to_str(self.get_main_packages_list(self.readable_running_distro))

            packages = main_packages + " " + user_packages
        else:
            packages = self.convert_list_to_str(pkglist)

        if self.readable_running_distro != "Arch Linux":
            raise NotImplementedError(f"{self.readable_running_distro}: this distro is not implemented yet")
        else:
            if current_user != "root":
                match package_manager:
                    case "apt":
                        cmd = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "pacman":
                        cmd = f"sudo {package_manager} -Syu --needed {packages}"
                    case "dnf":
                        cmd = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "paru":
                        cmd = f"{package_manager} -Syu --needed {packages}"
                    case "yay":
                        cmd = f"{package_manager} -Syu --needed {packages}"
                    case _:
                        raise NotImplementedError(f"{package_manager}: unknown package manager.")
            else:
                match package_manager:
                    case "apt":
                        cmd = f"{package_manager} update && sudo {package_manager} install {packages}"
                    case "pacman":
                        cmd = f"{package_manager} -Syu --needed {packages}"
                    case "dnf":
                        cmd = f"{package_manager} update && sudo {package_manager} install {packages}"
                    case _:
                        if package_manager == "paru" or package_manager == "yay":
                            raise ValueError(f"[!] AUR helpers like {package_manager} cannot be ran" +
                                             " as {current_user}.")
                        else:
                            raise NotImplementedError(f"{package_manager}: unknown package manager.")

        try:
            run(cmd, shell=True, universal_newlines=True, text=True)
        except Exception:
            raise
