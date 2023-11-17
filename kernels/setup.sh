#!/bin/sh		

case "$LINUX_DISTRO" in
    archlinux)
        if test ! -d "kernels/linux-tkg"
        then
            git -C "kernels" clone "https://github.com/frogging-family/linux-tkg.git"

            if test -f "kernels/linux-tkg/customization.cfg"
            then
                test $EDITOR && $EDITOR "kernels/linux-tkg/customization.cfg" || exit 1
            fi

            cd "kernels/linux-tkg" && ./install.sh install && cd "../.."
        else
            if test -f "kernels/linux-tkg/customization.cfg"
            then
                test $EDITOR && $EDITOR "kernels/linux-tkg/customization.cfg" || exit 1
            fi
            cd "kernels/linux-tkg" && git pull && ./install.sh && cd "../.."
        fi
    *)
        if test ! -d "kernels/linux-tkg"
        then
            git -C "kernels" clone "https://github.com/frogging-family/linux-tkg.git"

            if test -f "kernels/linux-tkg/customization.cfg"
            then
                test $EDITOR && $EDITOR "kernels/linux-tkg/customization.cfg" || exit 1
            fi

            cd "kernels/linux-tkg" && ./install.sh install && cd "../.."
        else
            if test -f "kernels/linux-tkg/customization.cfg"
            then
                test $EDITOR && $EDITOR "kernels/linux-tkg/customization.cfg" || exit 1
            fi
            cd "kernels/linux-tkg" && git pull && ./install.sh install && cd "../.."
        fi
    ;;
esac
