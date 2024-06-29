#!/usr/bin/env python3

from logging import log
import logging
import subprocess, shutil, getpass

class PackageManager():
    def __init__(self):
        self.lsb_release_bin: str | None = shutil.which("lsb_release")
        current_distro_cmd: subprocess.CompletedProcess[str] = subprocess.run("lsb_release -ds", shell=True, universal_newlines=True, capture_output=True, text=True)
        self.current_distro = current_distro_cmd.stdout.replace("\"", "").removesuffix("\n")
        self.current_user = getpass.getuser()
        
        if not self.lsb_release_bin:
            raise IOError("lsb_release: binary not found")

    def get_package_manager(self, overridePackageManager: bool = False) -> str:
        pm_bin: str

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

        if overridePackageManager:
            for pm in aur_helpers:
                if shutil.which(pm):
                    pm_bin = pm
                    break
        else:
            for pm in package_managers:
                if shutil.which(pm):
                    pm_bin = pm
                    break
 
        return pm_bin

    def install_aur_helper(self, distro: str, package_manager: str):
        if distro == "Arch Linux":
            if package_manager != "yay" or package_manager != "paru":
                raise ValueError(f"{package_manager} is not an AUR helper.")
        else:
            raise ValueError(f"{distro}: unsupported distribution.")

    def convert_list_to_str(self, list: list[str]) -> str:
        newlist = ' '.join(list)

        return newlist

    def get_main_packages_list(self) -> list[str]:
        if self.current_distro == "Arch Linux":
            arch_main: list[str] = [
                "alacritty",
                "apparmor",
                "archlinux-wallpaper",
                "bridge-utils",
                "bitwarden",
                "ccache",
                "chezmoi",
                "clamtk",
                "curl",
                "dnsmasq",
                "fail2ban",
                "fastfetch",
                "firefox",
                "firewalld",
                "fwupd",
                "gamemode",
                "github-cli",
                "git-lfs",
                "intel-ucode",
                "lib32-vulkan-mesa-layers",
                "libva-mesa-driver",
                "less",
                "linux",
                "linux-hardened",
                "linux-hardened-headers",
                "linux-headers",
                "linux-lts",
                "linux-lts-headers",
                "linux-zen",
                "linux-zen-headers",
                "lutris",
                "mesa-vdpau",
                "pacman-contrib",
                "papirus-icon-theme",
                "pipewire-alsa",
                "pipewire-pulse",
                "power-profiles-daemon",
                "qemu-desktop",
                "qt5-wayland",
                "qt6-wayland",
                "steam",
                "swtpm",
                "telegram-desktop",
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
            return arch_main
        else:
            raise ValueError(f"{self.current_distro} is not supported.")

    def get_package_list(self, only_get_aur: bool = False) -> list[str]:
        selected_pkglist: list[str]

        if self.current_distro == "Arch Linux":
            aur: list[str] = [
                "ananicy-git",
                "archlinux-artwork",
                "duckstation-git",
                "ckb-next-git",
                "github-desktop",
                "lib32-mangohud-git",
                "mangohud-git",
                "mkinitcpio-firmware",
                "pcsx2-git",
                "plymouth-theme-archlinux",
                "ppsspp-git",
                "preloader-signed",
                "rate-mirrors",
                "rpcs3-git",
                "spotify",
                "ttf-ubuntu-font-family"
                "ttf-meslo-nerd-font-powerlevel10k",
                "ventoy",
                "visual-studio-code-bin",
                "zsh-theme-powerlevel10k-git"
            ]

            arch_gnome: list[str] = [
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

            arch_kde: list[str] = [
                "bluedevil",
                "breeze-gtk",
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
                "powerdevil",
                "sddm"
            ]

            arch_xfce: list[str] = [
                "xfce4"
            ]

            if only_get_aur and self.current_distro == "Arch Linux":
                return aur
            else:
                user_choice: str = input("Choose a desktop environment [gnome/kde/xfce]: ")

            while True:
                match user_choice:
                    case "gnome":
                        selected_pkglist = arch_gnome
                        break
                    case "kde" | "plasma":
                        selected_pkglist =  arch_kde
                        break
                    case "xfce":
                        selected_pkglist =  arch_xfce
                        break
                    case _:
                        if user_choice.isalpha:
                            raise ValueError(f"{user_choice}: invalid desktop environment specified.")
                        else:
                            raise EOFError("no desktop environment was detected.")

        return selected_pkglist

    def install_packages(self, package_manager: str, custom_pkglist: list[str] = []) -> None:
        if custom_pkglist:
            pkglist: str = self.convert_list_to_str(custom_pkglist)
            packages: str = pkglist
        else:
            main_packages: list[str] = self.get_main_packages_list()
            main_pkglist: str = self.convert_list_to_str(main_packages)

            extra_packages: list[str] = self.get_package_list()
            pkglist: str = self.convert_list_to_str(extra_packages)

            aur_packages: list[str] = self.get_package_list(only_get_aur=True)
            aurlist: str = self.convert_list_to_str(aur_packages)

            packages: str = main_pkglist + " " + pkglist + " " + aurlist

        if self.current_distro != "Arch Linux":
            raise NotImplementedError(f"{self.current_distro}: such distro is not implemented yet")
        else:
            if self.current_user != "root":
                match package_manager:
                    case "apt":
                        cmd: str = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "pacman":
                        cmd: str = f"sudo {package_manager} -Syu --needed {packages}"
                    case "dnf":
                        cmd: str = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "paru":
                        if custom_pkglist:
                            cmd: str = f"{package_manager} -S --needed --sudoloop {packages}"
                        else:
                            cmd: str = f"{package_manager} -Syu --needed --sudoloop {packages}"
                    case "yay":
                        if custom_pkglist:
                            cmd: str = f"{package_manager} -S --needed --sudoloop {packages}"
                        else:
                            cmd: str = f"{package_manager} -Syu --needed --sudoloop {packages}"
                    case _:
                        raise NotImplementedError(f"{package_manager}: unknown package manager.")
            else:
                match package_manager:
                    case "apt":
                        cmd: str = f"{package_manager} update && sudo {package_manager} install {packages}"
                    case "pacman":
                        cmd: str = f"{package_manager} -Syu --needed {packages}"
                    case "dnf":
                        cmd: str = f"{package_manager} update && sudo {package_manager} install {packages}"
                    case _:
                        if package_manager == "paru" or package_manager == "yay":
                            raise PermissionError(f"{package_manager} is an AUR helper and it cannot be ran as "
                                                  + self.current_user)
                        else:
                            raise NotImplementedError(f"{package_manager}: unknown package manager.")
        try:
            subprocess.run(cmd, shell=True, universal_newlines=True, text=True)
        except Exception:
            raise
