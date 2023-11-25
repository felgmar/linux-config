#!/bin/sh

case $LINUX_DISTRO in
    arch|archlinux)
        if test ! -d "tools/linux-utils"
        then
            git -C "tools" clone https://gitlab.com/gfelipe099/linux-utils.git
            sudo sh "tools/linux-utils/archlinux-sbct"
        else
            git pull
            sudo sh "tools/linux-utils/archlinux-sbct"
        fi
    ;;
esac
