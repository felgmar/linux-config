#!/usr/bin/env python3

from subprocess import run

class ServicesManager():
    def get_services_list(self, pkglist: list[str]) -> list[str]:
        services = [
            "systemd-oomd.socket",
            "systemd-boot-update.service",
            "fail2ban.service",
            "apparmor.service",
            "firewalld.service",
            "ananicy.service",
            "bluetooth.service",
            "libvirtd.socket",
            "libvirtd-ro.socket",
            "libvirtd-admin.socket",
            "fancontrol.service",
            "cronie.service",
            "fstrim.timer",
            "clamav-freshclam.service"
        ]

        match pkglist:
            case "arch_gnome":
                services.append("gdm.service")

            case "arch_kde" | "arch_plasma":
                services.append("sddm.service")

            case "arch_xfce4":
                services.append("lightdm.service")

        return services

    def enable_service(self, services: str) -> None:
        for service in services:
            cmd = f"systemctl enable {service}"

            run(cmd, shell=True)
    
    def enable_services(self, services: list[str], user: str, verbose: bool = False) -> None:
        disabled_services: list[str] = []

        for service_name in services:
            service_status = run(f"systemctl is-enabled {service_name}", shell=True,
                                 universal_newlines=True, capture_output=True, text=True)
            readable_service_status = service_status.stdout.removesuffix("\n")

            if readable_service_status == "disabled":
                if verbose:
                    print(f"service: {service_name}, status: {readable_service_status}")

                disabled_services.append(service_name)
            else:
                raise Exception("There are no services left to enable from the list you specified.")

        for disabled_service in disabled_services:
            if user == "root":
                cmd = f"systemctl enable {disabled_service}"
            else:
                cmd = f"sudo systemctl enable {disabled_service}"
            
            run(cmd, shell=True)
