#!/usr/bin/env python3

"""
Module containing the PackageManager class.
"""

import subprocess
import shutil
import getpass

class PackageManager():
    """
    Manages the installation of packages.
    """
    def __init__(self):
        self.lsb_release_bin: str | None = shutil.which("lsb_release")
        current_distro_cmd: subprocess.CompletedProcess[str] = \
            subprocess.run("lsb_release -is", shell=True, universal_newlines=True,
                           capture_output=True, check=True, text=True)
        self.current_distro = current_distro_cmd.stdout.replace("\"", "").removesuffix("\n")
        self.current_user = getpass.getuser()

        if not self.lsb_release_bin:
            raise FileNotFoundError("lsb_release: not found")

    def get_package_manager(self, get_aur_helper: bool = False) -> str:
        """
        Returns the package manager based on the current distribution.
        """
        pm_bin: str | None = None

        package_managers = [
            "apt",
            "dnf",
            "pacman",
            "zypper"
        ]

        aur_helpers = [
            "paru",
            "yay"
        ]

        if get_aur_helper and not self.current_distro == "Arch":
            raise ValueError(f"Couldn't find any AUR helpers on {self.current_distro}")

        if get_aur_helper:
            for helper in aur_helpers:
                if not shutil.which(helper):
                    print(helper, "was not found")
                else:
                    pm_bin = helper
                    break
        else:
            for pm in package_managers:
                if shutil.which(pm):
                    pm_bin = pm
                    break

        if pm_bin is None:
            raise ValueError("No package manager could be set.")

        return pm_bin

    def install_aur_helper(self, distro: str, package_manager: str):
        """
        Installs an AUR helper based on the distribution.
        """
        match distro:
            case "Arch":
                match package_manager:
                    case "paru":
                        raise NotImplementedError()
                    case "yay":
                        raise NotImplementedError()
                    case _:
                        raise ValueError(package_manager, "invalid package manager")
            case _:
                raise ValueError(distro, ": unsupported distribution")

    def convert_list_to_str(self, list_to_convert: list[str]) -> str:
        """
        Converts a list to a string.
        """
        new_list = ' '.join(list_to_convert)

        return new_list

    def get_main_packages_list(self) -> list[str]:
        """
        Returns a list of main packages based on the current distribution.
        """
        match self.current_distro:
            case "Arch":
                pkglist = [
                    "7zip",
                    "alacritty",
                    "apparmor",
                    "archlinux-wallpaper",
                    "bridge-utils",
                    "bitwarden",
                    "ccache",
                    "clamtk",
                    "curl",
                    "dnsmasq",
                    "fail2ban",
                    "fastfetch",
                    "firewalld",
                    "fwupd",
                    "gamemode",
                    "github-cli",
                    "intel-ucode",
                    "lib32-gamemode",
                    "lib32-libpulse",
                    "lib32-vulkan-mesa-layers",
                    "libva-mesa-driver",
                    "lutris",
                    "mesa-vdpau",
                    "pacman-contrib",
                    "papirus-icon-theme",
                    "pipewire-alsa",
                    "pipewire-pulse",
                    "power-profiles-daemon",
                    "ppsspp",
                    "qemu-desktop",
                    "steam",
                    "swtpm",
                    "telegram-desktop",
                    "trash-cli",
                    "virt-manager",
                    "vulkan-mesa-layers",
                    "wine",
                    "wget",
                    "xdg-user-dirs",
                    "zram-generator",
                    "zsh",
                    "zsh-autosuggestions",
                    "zsh-completions",
                    "zsh-syntax-highlighting"
            ]
                return pkglist
            case _:
                raise ValueError(self.current_distro, "is not supported.")

    def get_desktop_environment(self) -> str:
        """
        Returns the desktop environment based on the user's choice.
        """
        desktop_environment = input("Choose a desktop environment [gnome/kde/xfce]: ")

        if not desktop_environment:
            raise ValueError("No desktop environment was specified.")

        match desktop_environment:
            case "gnome":
                return "gnome"
            case "kde" | "plasma":
                return "kde"
            case "xfce":
                return "xfce"
            case _:
                raise ValueError(desktop_environment, "invalid desktop environment")

    def get_package_list(self, desktop_environment: str, only_get_aur: bool = False) -> list[str]:
        """
        Returns a list of packages based on the desktop environment.
        """
        match self.current_distro:
            case "Arch":
                aur = [
                    "archlinux-artwork",
                    "duckstation-git",
                    "github-desktop",
                    "lib32-mangohud-git",
                    "mangohud-git",
                    "minq-ananicy-git",
                    "mkinitcpio-firmware",
                    "pcsx2-git",
                    "plymouth-theme-archlinux",
                    "preloader-signed",
                    "protonup-rs",
                    "rate-mirrors",
                    "rpcs3-git",
                    "spotify",
                    "ventoy-bin",
                    "visual-studio-code-bin",
                ]

                gnome = [
                    "gdm",
                    "gnome-backgrounds",
                    "gnome-browser-connector",
                    "gnome-control-center",
                    "gnome-disk-utility",
                    "gnome-keyring",
                    "gnome-themes-extra",
                    "gvfs",
                    "gvfs-mtp",
                    "gvfs-nfs",
                    "gvfs-google",
                    "libappindicator-gtk3",
                    "malcontent",
                    "nautilus"
                ]

                kde = [
                    "bluedevil",
                    "breeze-gtk",
                    "dolphin",
                    "gnome-keyring",
                    "kde-gtk-config",
                    "kdialog",
                    "kscreen",
                    "kwalletmanager",
                    "kwallet-pam",
                    "plasma-desktop",
                    "plasma-nm",
                    "plasma-pa",
                    "powerdevil",
                    "sddm"
                ]

                xfce = [
                    "xfce4"
                ]
            case _:
                raise ValueError(self.current_distro, "unsupported distro")

        if only_get_aur and self.current_distro == "Arch":
            return aur

        match desktop_environment:
            case "gnome":
                return gnome
            case "kde" | "plasma" | "kdeplasma":
                return kde
            case "xfce":
                return xfce
            case _:
                raise ValueError(desktop_environment, "invalid desktop environment")

    def install_packages(self, package_manager: str,
                         desktop_environment: str,
                         custom_pkglist: list[str] | None) -> None:
        """
        Installs packages based on the current distribution.
        """
        packages: str | None = None
        cmd: str = ""

        if not custom_pkglist is None:
            packages = self.convert_list_to_str(custom_pkglist)
        else:
            main_packages = self.get_main_packages_list()
            main_pkglist = self.convert_list_to_str(main_packages)

            extra_packages = self.get_package_list(desktop_environment)
            extra_pkglist = self.convert_list_to_str(extra_packages)

            match self.current_distro:
                case "Arch":
                    aur_packages = self.get_package_list(desktop_environment,
                                                         only_get_aur=True)
                    aur_pkglist = self.convert_list_to_str(aur_packages)
                    packages = main_pkglist + " " + extra_pkglist + " " + aur_pkglist
                case _:
                    packages = main_pkglist + " " + extra_pkglist + " "

        if self.current_user == "root":
            match package_manager:
                case "apt":
                    cmd = f"{package_manager} update &&" + \
                          f"{package_manager} install {packages}"
                case "pacman":
                    cmd = f"{package_manager} -Syu --needed {packages}"
                case "dnf":
                    cmd = f"{package_manager} update &&" \
                          f"{package_manager} install {packages}"
                case "paru" | "yay":
                    raise PermissionError(package_manager,
                                          "is an AUR helper and it cannot be ran as " +
                                          self.current_user)
                case _:
                    raise NotImplementedError(package_manager, "unknown package manager.")
        else:
            match package_manager:
                case "apt":
                    cmd = f"sudo {package_manager} update &&" + \
                          f"sudo {package_manager} install {packages}"
                case "pacman":
                    cmd = f"sudo {package_manager} -Syu --needed {packages}"
                case "dnf":
                    cmd = f"sudo {package_manager} update &&" \
                          f"sudo {package_manager} install {packages}"
                case "paru" | "yay":
                    if custom_pkglist:
                        cmd = f"{package_manager} -S --needed --sudoloop {packages}"
                    else:
                        cmd = f"{package_manager} -Syu --needed --sudoloop {packages}"
                case _:
                    raise NotImplementedError(package_manager, "unknown package manager.")

        try:
            subprocess.run(cmd, shell=True, universal_newlines=True, check=True, text=True)
        except Exception as e:
            raise e
