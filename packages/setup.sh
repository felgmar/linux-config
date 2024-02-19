#!/bin/sh
set -e

if test -z "${LINUX_DISTRO}"
then
    echo "error: no distribution was specified"
    exit 1
fi

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
            case "$desktop_environment" in
                gnome)      paru -S --needed $(cat packages/gnome_pkglist) && break;;
                kde|plasma) paru -S --needed $(cat packages/kde_pkglist) && break;;
                xfce)       paru -S --needed $(cat packages/xfce_pkglist) && break;;
                *)          echo "Unknown desktop environment $desktop_environment"; exit 1;;
            esac
        fi

        test -f packages/aur && paru -S --needed $(cat packages/aur) || exit 1
        test -f packages/pkglist && paru -S --needed $(cat packages/pkglist) || exit 1

	desktop_environment="$desktop_environment" ./tools/setup-services.sh || exit 1

        if test "$(plymouth-set-default-theme -l | grep archlinux)"
        then
            sudo plymouth-set-default-theme -R archlinux
        else
            echo "ERROR: no archlinux plymouth theme was found"
        fi
    ;;
    kubuntu)
        sudo apt purge --autoremove partitionmanager kup-backup plasma-discover konqueror kate kwrite kfind plasma-welcome zutty konsole plasma-widgets-addons mahjongg kmines kpat ksudoku gwenview okular skanlite konversation krdc ktorrent thunderbird elisa haruna pavucontrol-qt ksystemlog ksystemstats xterm kcalc usb-creator-kde kde-spectacle info plasma-vault qsynth
    ;;
    *) echo "error: $LINUX_DISTRO: unknown error" && exit 1;;
esac

