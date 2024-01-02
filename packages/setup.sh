#!/bin/sh
set -e

case $LINUX_DISTRO in
    archlinux)
        test ! -x "$(command -v ccache)" && sudo pacman -Syu ccache --needed --noconfirm
        test ! -x "$(command -v git)" && sudo pacman -Syu git --needed --noconfirm

        if test ! -x "$(command -v paru)" && test ! -d "packages/paru"
        then
            git -C "packages" clone "https://aur.archlinux.org/paru.git"
            cd "packages/paru" && makepkg -cCisr && cd "../.."
        fi

        read -p "Choose a desktop environment [gnome/kde/xfce]: " desktop_environment
        if test -z "${desktop_environment}"
        then
            echo "No desktop environment was specified, falling back to 'gnome'."
            desktop_environment="gnome"
            paru -S --needed $(cat packages/gnome_pkglist)
        else
            case $desktop_environment in
                gnome)      paru -S --needed $(cat packages/gnome_pkglist) && break;;
                kde|plasma) paru -S --needed $(cat packages/kde_pkglist) && break;;
                xfce)       paru -S --needed $(cat packages/xfce_pkglist) && break;;
                *)          echo "Unknown desktop environment $desktop_environment"; exit 1;;
            esac
        fi

        test -f packages/aur && paru -S --needed $(cat packages/aur) || exit 1
        test -f packages/pkglist && paru -S --needed $(cat packages/pkglist) || exit 1

        if test "$(plymouth-set-default-theme -l | grep archlinux)"
        then
            sudo plymouth-set-default-theme -R archlinux
        else
            echo "ERROR: no archlinux plymouth theme was found"
        fi
    ;;
    debian)
        main_packages=(
            sddm
            kde-gtk-config
            plasma-desktop
        )
        extra_packages=(
            firefox
            papirus-icon-theme
            systemd-timesyncd
            git
            zsh
            curl
            wget
            zsh
            zsh-autosuggestion
            zsh-syntax-highlighting
            spotify-client
            code
            steam
            virt-manager
            chezmoi
            lutris
            wine-staging
            power-profiles-daemon
            bluez-firmware
            gdisk
            gnome-disk-utility
            zram-generator
            kitty
        )
        packages_to_remove=(
            partitionmanager
            kup-backup
            discover
            konqueror
            kate
            kwrite
            kfind
            plasma-welcome
            zutty
            plasma-discover
            konsole
        )
        echo sudo apt install ${main_packages[@]}
        echo sudo apt install ${extra_packages[@]}
        echo sudo apt purge --autoremove ${packages_to_remove[@]}
    ;;
esac
