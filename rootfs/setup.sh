#!/bin/sh

omzi()
{
    test -z $1 && echo "No command specified" && exit 1
    while getopts 'iru' arg
    do
        case "$arg" in
            i)
                curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | "`command -v zsh`"
                git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
                    ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
                test -f "rootfs/home/.zshrc" && cat "rootfs/home/.zshrc" | tee -a "$HOME/.zshrc" || exit 1
                test $? = 0 && `command -v zsh` -c ". $HOME/.zshrc && omz theme set powerlevel10k/powerlevel10k"
                printf "\nPlease restart the terminal to configure powerlevel10k or run the command 'p10k configure'\n"
                exit $?
            ;;
            r)
                test -d "$HOME/.oh-my-zsh" && rm -rfv "$HOME/.oh-my-zsh"
                curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh | "`command -v zsh`"
                git clone --depth=1 https://github.com/romkatv/powerlevel10k.git \
                    ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
                test -f "rootfs/home/.zshrc" && cat "rootfs/home/.zshrc" | tee -a "$HOME/.zshrc" || exit 1
                test $? = 0 && `command -v zsh` -c ". $HOME/.zshrc && omz theme set powerlevel10k/powerlevel10k"
                printf "\nPlease restart the terminal to configure powerlevel10k or run the command 'p10k configure'\n"
                exit $?
            ;;
            u)
                test -d $HOME/.oh-my-zsh && rm $HOME/.oh-my-zsh; exit $?
            ;;
            ?) echo "Unknown command: $arg" && exit 1
            ;;
        esac
    done
}

if test ! -d "/boot/loader/entries-backup"
then
    sudo mkdir -pv "/boot/loader/entries-backup"
fi

echo ":: Backing up current bootloader entries..."
find /boot/loader/entries/ -type f -exec sudo cp -v {} /boot/loader/entries-backup/ \;

echo ":: Backing up pacman mirror list..."
find /etc/pacman.d/mirrorlist -type f -exec echo sudo cp -v {} {}.backup.$(date +%m-%d-%y) \;

echo ":: Copying files..."
find rootfs/boot/ -type d -exec sudo cp -rv {} "/boot/" \;
find rootfs/etc/ -type d -exec sudo cp -rv {} "/etc/" \;
find rootfs/home/.config -type d -exec cp -rv {} "$HOME/.config/" \;
find rootfs/home/.ssh -type d -exec cp -rv {} "$HOME/.ssh" \;
find rootfs/home/.makepkg.conf -type f -exec cp -v {} "$HOME/.makepkg.conf" \;
find rootfs/home/.zshrc -type f -exec cat {} >> "$HOME/.zshrc" \; 

lsblk || exit 1

read -p ":: Where is the root partition mounted at? (e.g. /dev/sda1): " root_device
if test -z "${root_device}"
then
    echo ":: ERROR: No root device was specified" && exit 1
else
    if test -z "$(sudo blkid -s PARTUUID -o value ${root_device})"
    then
        echo ":: ERROR: ${root_device}: invalid device" && exit 1
    else
        if test -f "/etc/kernel/cmdline"
        then
            sudo sed "s,<enter_partuuid_here>,`sudo blkid -s PARTUUID -o value $root_device`,g" -i "/etc/kernel/cmdline"
        fi
    fi
fi

if test $(command -v zsh)
then
    if test ! -d "$HOME/pretty-terminals"
    then
        git -C "$HOME" clone https://gitlab.com/gfelipe099/pretty-terminals.git
        cd "$HOME/pretty-terminals"
        sh pretty-terminals -t kitty
        cd "$HOME"
    else
        cd "$HOME/pretty-terminals"
        git pull --rebase
        sh pretty-terminals -t kitty
        cd "$HOME"
    fi
else
    case $LINUX_DISTRO in
        archlinux|arch) sudo pacman -S zsh --needed --noconfirm;;
        debian|ubuntu) sudo apt install -y zsh;;
        *) echo "error: $LINUX_DISTRO: unknown distribution"; exit 1;;
    esac

    if test ! -d "$HOME/pretty-terminals"
    then
        git -C "$HOME" clone https://gitlab.com/gfelipe099/pretty-terminals.git
        cd "$HOME/pretty-terminals"
        sh pretty-terminals -t kitty
        cd "$HOME"
    else
        cd "$HOME/pretty-terminals"
        git pull --rebase
        sh pretty-terminals -t kitty
        cd "$HOME"
    fi
fi
