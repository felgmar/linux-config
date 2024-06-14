#!/usr/bin/env python3
import shutil
from subprocess import run

class PackageManager():
    def __init__(self):
        self.lsb_release_path = shutil.which("lsb_release")

        if not self.lsb_release_path:
            raise ValueError("could not find the file lsb_release.")

        self.running_distro = run("lsb_release -ds", shell=True,
                                  universal_newlines=True, capture_output=True, text=True)
        self.readable_running_distro = self.running_distro.stdout.replace("\"", "").removesuffix("\n")

    def get_package_manager(self, distro: str, overridePackageManager: bool = False) -> str:
        pm_bin: str = None

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
            return pm_bin
        else:
            for pm in package_managers:
                if shutil.which(pm):
                    pm_bin = pm
                    break
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
                "alacritty",
                "apparmor",
                "archlinux-wallpaper",
                "bridge-utils",
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
                "keepassxc",
                "lib32-vulkan-mesa-layers",
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
                "ttf-meslo-nerd-font-powerlevel10k",
                "virt-manager",
                "vulkan-mesa-layers",
                "wine-staging",
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

    def get_package_list(self, distro: str, only_get_aur: bool = False) -> list[str]:
        if distro == "Arch Linux":
            aur = [
                "ananicy-git",
                "archlinux-artwork",
                "duckstation-git",
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
                "ventoy",
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
                "gnome-themes-extra",
                "gvfs",
                "gvfs-mtp",
                "gvfs-nfs",
                "gvfs-google",
                "libappindicator-gtk3",
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
                "powerdevil",
                "sddm"
            ]

            arch_xfce = [
                "xfce4"
            ]

            if only_get_aur and self.readable_running_distro == "Arch Linux":
                selected_pkglist: str = aur
                return selected_pkglist
            else:
                selected_pkglist: str = str(input("Choose a desktop environment [gnome/kde/xfce]: "))
        else:
            raise ValueError(f"[!] {distro} is not supported.")

        while True:
            match selected_pkglist:
                case "gnome":
                    selected_pkglist: str = arch_gnome
                    break
                case "kde" | "plasma":
                    selected_pkglist: str =  arch_kde
                    break
                case "xfce":
                    selected_pkglist: str =  arch_xfce
                    break
                case _:
                    if selected_pkglist != "":
                        raise ValueError(f"{selected_pkglist}: invalid list specified.")
                    else:
                        raise EOFError("no output was detected.")

        return selected_pkglist

    def install_packages(self, package_manager: str, current_user: str, additional_pkglist: list[str] = []) -> None:
        main_packages: str = self.get_main_packages_list(self.readable_running_distro)
        main_pkglist: str = self.convert_list_to_str(main_packages)

        extra_packages: str = self.get_package_list(self.readable_running_distro)
        pkglist: str = self.convert_list_to_str(extra_packages)

        aur_packages: str = self.get_package_list(self.readable_running_distro, only_get_aur=True)
        aurlist: str = self.convert_list_to_str(aur_packages)

        if additional_pkglist:
            aux_pkglist: str = self.convert_list_to_str(additional_pkglist)
            packages: str = aux_pkglist
        else:
            packages: str = main_pkglist + " " + pkglist + " " + aurlist

        if self.readable_running_distro != "Arch Linux":
            raise NotImplementedError(f"{self.readable_running_distro}: such distro is not implemented yet")
        else:
            if current_user != "root":
                match package_manager:
                    case "apt":
                        cmd: str = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "pacman":
                        cmd: str = f"sudo {package_manager} -Syu --needed {packages}"
                    case "dnf":
                        cmd: str = f"sudo {package_manager} update && sudo {package_manager} install {packages}"
                    case "paru":
                        cmd: str = f"{package_manager} -Syu --needed --sudoloop {packages}"
                    case "yay":
                        cmd: str = f"{package_manager} -Syu --needed {packages}"
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
                            raise ValueError(f"[!] AUR helpers like {package_manager} cannot be ran" +
                                             " as {current_user}.")
                        else:
                            raise NotImplementedError(f"{package_manager}: unknown package manager.")
        try:
            run(cmd, shell=True, universal_newlines=True, text=True)
        except Exception:
            raise
