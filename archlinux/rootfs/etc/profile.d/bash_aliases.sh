#!/bin/sh

# detailed file and directory listing
alias ll='ls -alih --color=auto'
alias ls='ls --color=auto'

# apt-like pacman wrapper
pkg()
{
    test -z $1 && echo "Usage: `basename $0` [install|update|upgrade|purge|search|clean]" && return 1

    case $1 in
        install) shift; sudo pacman -S --needed "$@"; return $?;;
        remove) shift; sudo pacman -Rsu "$@"; return $?;;
        update) shift; sudo pacman -Sy --needed; return $?;;
        upgrade) shift; sudo pacman -Syu --needed; return $?;;
        purge) shift; sudo pacman -Rncsd "$@"; return $?;;
        search) shift; pacman -Ss "$@"; return $?;;
        clean) shift; sudo pacman -Rncsd $(pacman -Qqtd); return $?;;
        *) test ! -z $1 && echo "Unknown command: $1"; return $?;;
    esac
}

# others
alias update-initramfs='sudo mkinitcpio -P'
alias yay='test $(whoami) = "root" && echo "Do not run yay as root" || sudo -u $(whoami) yay'
