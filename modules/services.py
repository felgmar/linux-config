#!/usr/bin/env python3

"""
Module containing the ServicesManager class.
"""

import getpass
import subprocess

class ServicesManager():
    """
    Manages services using systemctl.
    """
    def __init__(self):
        self.current_user = getpass.getuser()

    def get_services_list(self, desktop_environment: str | None) -> list[str]:
        """
        Returns a list of services based on the desktop environment.
        """
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

        match desktop_environment:
            case "gnome":
                services.append("gdm.service")
            case "kde" | "plasma" | "kde_plasma":
                services.append("sddm.service")
            case "xfce":
                services.append("lightdm.service")
            case _:
                print("[INFO] No desktop environment was specified.")
        return services

    def enable_service(self, service: str) -> None:
        """
        Enable a service using systemctl.
        """
        if self.current_user == "root":
            cmd: str = f"systemctl enable {service}"
        else:
            cmd: str = f"sudo systemctl enable {service}"

        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            raise e

    def enable_services(self, services: list[str], verbose: bool = False) -> None:
        """
        Enable a list of services using systemctl.
        """
        disabled_services: list[str] = []

        for service_name in services:
            service_status: subprocess.CompletedProcess[str] = \
                subprocess.run(f"systemctl is-enabled {service_name}", shell=True,
                               universal_newlines=True, capture_output=True,
                               text=True)
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
            except Exception as e:
                raise e
