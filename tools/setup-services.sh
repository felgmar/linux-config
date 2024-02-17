#!/bin/sh

services=('systemd-oomd.socket'
          'systemd-boot-update.service'
          'fail2ban.service'
          'apparmor.service'
          'firewalld.service'
          'ananicy.service'
          'bluetooth.service'
          'libvirtd.socket'
          'libvirtd-ro.socket'
          'libvirtd-admin.socket'
          'fancontrol.service'
          'cronie.service'
          'fstrim.timer'
          'clamav-freshclam.service')

case "${LINUX_DISTRO}" in
    archlinux|arch)
        for service in "${services[@]}"
        do
            if test "$(systemctl is-enabled "${service}")" != "enabled"
            then
                sudo systemctl enable --now "${service}"
                if test "${service}" = "gdm.service"
                then
                    sudo systemctl enable "${service}"
                else
                    sudo systemctl enable --now "${service}"
                fi
            else
                echo "WARNING: "${service}" is already enabled"
                test "${service}" = "gdm.service" && break
                if test "$(systemctl is-active "${service}")" != "active"
                then
                    echo "WARNING: Starting the service "${service}"..."
                    sudo systemctl start "${service}"
                fi
            fi
        done

        if test "$(systemctl get-default)" != "graphical.target"
        then
            sudo systemctl set-default graphical.target || exit 1
        fi
    ;;
    *)
        echo "error: ${LINUX_DISTRO}: there are no extra services to enable for such distro yet"
        exit 1
    ;;
esac
