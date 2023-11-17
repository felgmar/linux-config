#!/bin/sh

if test ! -d "tools/linux-utils"
then
    git -C "tools" clone https://gitlab.com/mrkenhoo/linux-utils.git
    sudo sh "tools/linux-utils/archlinux-sbct"
else
    git pull
    sudo sh "tools/linux-utils/archlinux-sbct"
fi
