#!/bin/sh

case "${LINUX_DISTRO}" in
    archlinux)
        echo ":: Backing up bootloader entries..."
        if test ! -d "/boot/loader/entries-backup"
        then
            sudo mkdir -pv "/boot/loader/entries-backup"
        fi
        sudo mv -v --target-directory=/boot/loader/entries-backup /boot/loader/entries/*.conf \;

        echo ":: Backing up pacman mirror list..."
        sudo cp -v /etc/pacman.d/mirrorlist /etc/pacman.d/mirrorlist.backup.$(date +%m-%d-%y) \;

        if test -f "/boot/loader/loader.conf"
        then
            echo ":: Backing up systemd-boot configuration..."
            sudo cp --target-directory=/boot/loader-backup /boot/loader/loader.conf
        fi

        echo ":: Backing up /etc/mkinitcpio.d directory..."
        if test ! -d /etc/mkinitcpio.d.backup
        then
            sudo mkdir -v /etc/mkinitcpio.d.backup
        fi
	for f in /etc/mkinitcpio.d/*.preset
        do
            sudo mv -v $f /etc/mkinitcpio.d.backup/${f}.$(date +%m-%d-%y_%T)
        done

	if test -f /etc/kernel/cmdline
        then
            echo ":: Backing up /etc/kernel/cmdline file..."
            sudo cp -v /etc/kernel/cmdline /etc/kernel/cmdline.backup
        fi

        echo ":: Copying files..."
        sudo cp -v --target-directory=/etc/kernel rootfs/etc/kernel/cmdline
        sudo cp -v --target-directory=/etc/libvirt/hooks rootfs/etc/libvirt/hooks/qemu
        sudo cp -v --target-directory=/etc/mkinitcpio.conf.d rootfs/etc/mkinitcpio.conf.d/custom.conf
        sudo cp -v --target-directory=/etc/mkinitcpio.d rootfs/etc/mkinitcpio.d/linux-hardened.preset
        sudo cp -v --target-directory=/etc/mkinitcpio.d rootfs/etc/mkinitcpio.d/linux-lts.preset
        sudo cp -v --target-directory=/etc/mkinitcpio.d rootfs/etc/mkinitcpio.d/linux-tkg.preset
        sudo cp -v --target-directory=/etc/mkinitcpio.d rootfs/etc/mkinitcpio.d/linux-zen.preset
        sudo cp -v --target-directory=/etc/mkinitcpio.d rootfs/etc/mkinitcpio.d/linux.preset
        sudo cp -v --target-directory=/etc/modprobe.d rootfs/etc/modprobe.d/kvm.conf
        sudo cp -v --target-directory=/etc/modprobe.d rootfs/etc/modprobe.d/snd_hda_intel.conf
        sudo cp -v --target-directory=/etc/modprobe.d rootfs/etc/modprobe.d/vfio.conf
        sudo cp -v --target-directory=/etc/profile.d rootfs/etc/profile.d/bash_aliases.sh
        sudo cp -v --target-directory=/etc/sysctl.d rootfs/etc/sysctl.d/99-vm-zram-parameters.conf
        sudo cp -v --target-directory=/etc/sysctl.d rootfs/etc/sysctl.d/100-enable-sysrq.conf
        sudo cp -v --target-directory=/etc/systemd rootfs/etc/systemd/zram-generator.conf
        sudo cp -v --target-directory=/etc/ rootfs/etc/environment
        sudo cp -v --target-directory=/etc/ rootfs/etc/locale.conf
        sudo cp -v --target-directory=${HOME} rootfs/home/.config/modprobed.db
        sudo cp -v --target-directory=${HOME} rootfs/home/.ssh/config
        sudo cp -v --target-directory=${HOME} rootfs/home/.makepkg.conf
    ;;
esac

read -p "Is your root partition encrypted?: " root_device_is_encrypted
lsblk || exit 1

read -p ":: Where is the root partition mounted at? (e.g. /dev/sda1): " root_device
case "${root_device}" in
    "/dev/"*)
        root_device_partuuid="$(sudo blkid -s PARTUUID -o value ${root_device})"
        if test -z "${root_device_partuuid}"
        then
            echo ":: ERROR: ${root_device}: invalid device" && exit 1
        else
            if test -f "/etc/kernel/cmdline"
            then
                sudo sed "s,<enter_partuuid_here>,${root_device_partuuid},g" -i "/etc/kernel/cmdline"
            fi
        fi
    ;;
    *)
        echo ":: ERROR: No root device was specified"
        exit 1
    ;;
esac

if test -x "$(command -v zsh)"
then
    if test ! -d "${HOME}/pretty-terminals"
    then
        git -C "${HOME}" clone https://gitlab.com/gfelipe099/pretty-terminals.git "${HOME}/.cache"
        cd "${HOME}/pretty-terminals"
        sh pretty-terminals -t kitty
        cd "${HOME}"
    else
        cd "${HOME}/pretty-terminals"
        git pull --rebase
        sh pretty-terminals -t kitty
        cd "${HOME}"
    fi
else
    case $LINUX_DISTRO in
        archlinux|arch) sudo pacman -S zsh --needed --noconfirm;;
        debian|ubuntu)  sudo apt install -y zsh;;
        *)              echo "error: $LINUX_DISTRO: unknown distribution"; exit 1;;
    esac

    if test ! -d "${HOME}/.cache/pretty-terminals"
    then
        git clone https://gitlab.com/gfelipe099/pretty-terminals.git "${HOME}/.cache/pretty-terminals"
        cd "${HOME}/.cache/pretty-terminals"
        sh pretty-terminals -t kitty
        cd "${HOME}"
    else
        cd "${HOME}/.cache/pretty-terminals"
        git pull --rebase
        sh pretty-terminals -t kitty
        cd "${HOME}"
    fi
fi
