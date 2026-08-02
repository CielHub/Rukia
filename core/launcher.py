"""
launcher.py
CARRERA-HUB v2
Core Launcher
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

PACKAGE_CONFIG = Path("selected_packages.json")
SERVER_CONFIG = Path("private_server.json")


class Launcher:

    def __init__(self):
        self.packages = []
        self.deeplink = ""

    def load_packages(self):
        if not PACKAGE_CONFIG.exists():
            raise FileNotFoundError("selected_packages.json not found.")

        data = json.loads(PACKAGE_CONFIG.read_text(encoding="utf-8"))
        self.packages = data.get("packages", [])
        return self.packages

    def load_deeplink(self):
        if not SERVER_CONFIG.exists():
            raise FileNotFoundError("private_server.json not found.")

        data = json.loads(SERVER_CONFIG.read_text(encoding="utf-8"))
        self.deeplink = data.get("deeplink", "")
        return self.deeplink

    def launch_package(self, package: str):
        subprocess.run(
            [
                "am",
                "start",
                "-n",
                f"{package}/com.roblox.client.startup.ActivitySplash",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    def open_deeplink(self):
        subprocess.run(
            [
                "am",
                "start",
                "-a",
                "android.intent.action.VIEW",
                "-d",
                self.deeplink,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )

    def start(self, launch_delay: float = 5.0):
        self.load_packages()
        self.load_deeplink()

        for package in self.packages:
            print(f"[Launcher] Starting {package}")
            self.launch_package(package)
            time.sleep(launch_delay)

            print(f"[Launcher] Opening Private Server")
            self.open_deeplink()

            time.sleep(3)


if __name__ == "__main__":
    Launcher().start()
  
