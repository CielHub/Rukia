"""
launcher.py
CARRERA-HUB v2
Bug Fix Revision
"""

from __future__ import annotations

import json
import subprocess
import time
from pathlib import Path

PACKAGE_CONFIG = Path("selected_packages.json")
SERVER_CONFIG = Path("private_server.json")


class Launcher:

    def __init__(self, launch_delay=6.0, debug=True):
        self.launch_delay = launch_delay
        self.debug = debug
        self.packages = []
        self.deeplink = ""

    def _run(self, command):
        result = subprocess.run(command, capture_output=True, text=True, check=False)
        if self.debug:
            print("\n[DEBUG]", " ".join(command))
            print("[EXIT]", result.returncode)
            if result.stdout.strip():
                print(result.stdout.strip())
            if result.stderr.strip():
                print(result.stderr.strip())
        return result

    def load_packages(self):
        self.packages = json.loads(PACKAGE_CONFIG.read_text()).get("packages", [])
        return self.packages

    def load_deeplink(self):
        self.deeplink = json.loads(SERVER_CONFIG.read_text()).get("deeplink", "")
        return self.deeplink

    def launch_package(self, package):
        self._run(["monkey","-p",package,"-c","android.intent.category.LAUNCHER","1"])

    def open_deeplink(self, package):
        self._run([
            "am","start","-W",
            "-a","android.intent.action.VIEW",
            "-d",self.deeplink,
            package
        ])

    def start(self):
        self.load_packages()
        self.load_deeplink()

        for package in self.packages:
            print(f"[Launcher] Launching {package}")
            self.launch_package(package)
            time.sleep(self.launch_delay)
            print(f"[Launcher] Opening deeplink for {package}")
            self.open_deeplink(package)
            time.sleep(2)

if __name__ == "__main__":
    Launcher().start()
    
