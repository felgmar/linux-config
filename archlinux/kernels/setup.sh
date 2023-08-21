#!/bin/sh		

if test ! -d "kernels/linux-tkg"
then
    git -C "kernels" clone "https://github.com/frogging-family/linux-tkg.git"

    if test -f "kernels/customization.patch"
    then
        patch -p 1 "kernels/linux-tkg/customization.cfg" "kernels/customization.patch" --posix
    else
        echo "WARNING: customization.patch: file not found"
        exit 1
    fi

    test ! $(command -v patch) && sudo pacman -Sy --needed --noconfirm "base-devel"

    cd "kernels/linux-tkg" && makepkg -cirs --needed && cd "../.."
else
    cd "kernels/linux-tkg" && git pull && makepkg -cirsf && cd "../.."
fi
