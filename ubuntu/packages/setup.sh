#!/bin/sh
set -e

echo "These Ubuntu flavors are supported by this script:
  - Ubuntu
  - Kubuntu
  - Xubuntu"

read -p "Which one do you want to install? [ubuntu/kubuntu/xubuntu]: " ubuntu_flavor
if test -z "$ubuntu_flavor"
then
    echo "No Ubuntu flavor was specified, falling back to 'ubuntu'."
    sudo apt install -y ubuntu-desktop-minimal || exit 1
else
    case "$ubuntu_flavor" in
        ubuntu)   sudo apt install -y ubuntu-desktop-minimal && break;;
        kubuntu)  sudo apt install -y kde-plasma-desktop && break;;
        xubuntu)  sudo apt install -y xubuntu-core && break;;
        *) echo "error: $ubuntu_flavor: unknown Ubuntu flavor" && exit 1;;
    esac
fi

test -f "packages/pkglist" && sudo apt install -y $(cat packages/pkglist) || exit 1
