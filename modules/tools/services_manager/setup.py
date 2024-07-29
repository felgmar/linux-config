#!/usr/bin/env python3

import getpass, subprocess

class ServicesManager():
    def __init__(self):
        self.current_user = getpass.getuser()
    
    def get_services_list(self, pkglist: list[str]) -> list[str]:
        services: list[str] = [
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

            case "arch_xfce":
                services.append("lightdm.service")

        return services

    def enable_service(self, service: str) -> None:
        if self.current_user == "root":
            cmd: str = f"systemctl enable {service}"
        else:
            cmd: str = f"sudo systemctl enable {service}"

        try:
            subprocess.run(cmd, shell=True)
        except:
            raise
    
    def enable_services(self, services: list[str], verbose: bool = False) -> None:
        disabled_services: list[str] = []

        for service_name in services:
            service_status: subprocess.CompletedProcess[str] = subprocess.run(f"systemctl is-enabled {service_name}", shell=True, universal_newlines=True, capture_output=True, text=True)
            readable_service_status: str = service_status.stdout.removesuffix("\n")

            if readable_service_status == "disabled":
                if verbose:
                    print(f"service: {service_name}, status: {readable_service_status}")

                disabled_services.append(service_name)
            else:
                print(f"{service_name} is {readable_service_status}")

        for disabled_service in disabled_services:
            try:
                self.enable_service(disabled_service)
            except:
                raise
