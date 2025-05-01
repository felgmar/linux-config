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

    def __get_services_list(self, desktop_environment: str) -> list[str]:
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
                raise ValueError(f"{desktop_environment}: invalid or unrecognized desktop environment")

        return services

    def __get_disabled_services(self, services: list[str], verbose: bool = False) -> dict[str, str]:
        """
        Retrieves a dictionary with all the services that are disabled.
        """
        disabled_services: dict[str, str] = {}

        for service_name in services:
            service_status: str = \
                subprocess.run(f"systemctl is-enabled {service_name}", shell=True,
                               universal_newlines=True, capture_output=True, check=False,
                               text=True).stdout.removesuffix("\n")

            match service_status:
                case "disabled":
                    if verbose:
                        print("service:", service_name, "status:", service_status)
                    try:
                        disabled_services[service_name] = service_status
                    except Exception as e:
                        raise e
                case "enabled":
                    if verbose:
                        print(f"{service_name} is already {service_status}")
                case _:
                    raise Exception(f"An error occurred with {service_name}. Status: {service_status}")
        
        return disabled_services

    def enable_service(self, service: str) -> None:
        """
        Enable a service using systemctl.
        """
        match self.current_user:
            case "root":
                cmd: str = f"systemctl enable {service}"
            case _:
                cmd: str = f"sudo systemctl enable {service}"
        try:
            subprocess.run(cmd, shell=True, check=True)
        except Exception as e:
            raise e

    def enable_services(self, desktop_environment: str, verbose: bool = False) -> None:
        """
        Enable a list of services using systemctl.
        """
        services_list = self.__get_services_list(desktop_environment)
        services_to_enable = self.__get_disabled_services(services_list, verbose)

        for name, status in services_to_enable.items():
            try:
                match status:
                    case "disabled":
                        if verbose:
                            print(f"[VERBOSE] {name}, status: {status}")
                        self.enable_service(name)
                    case _:
                        print(f"An error occurred with the service {name}. Status: {status}.")
            except Exception as e:
                raise e
