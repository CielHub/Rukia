"""
package_manager.py
CARRERA-HUB v2
Core Package Manager
"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

CONFIG_FILE = Path("selected_packages.json")


class PackageManager:

    def __init__(self):
        self.packages = []
        self.selected = []

    def scan(self):
        """Scan installed Roblox packages (Android/Termux)."""
        self.packages.clear()
        try:
            result = subprocess.run(
                ["pm", "list", "packages"],
                capture_output=True,
                text=True,
                check=False,
            )
            for line in result.stdout.splitlines():
                pkg = line.replace("package:", "").strip()
                if "roblox" in pkg.lower():
                    self.packages.append(pkg)
        except Exception:
            pass
        return self.packages

    def display(self):
        print("\n=== Roblox Packages ===")
        if not self.packages:
            print("No Roblox packages found.")
            return
        for i, pkg in enumerate(self.packages, 1):
            print(f"[{i}] {pkg}")
        print("[A] Select All")

    def select(self):
        if not self.packages:
            return []

        choice = input("\nSelect (example: 1,2,4 or A): ").strip().upper()

        if choice == "A":
            self.selected = list(self.packages)
        else:
            indexes = []
            for item in choice.split(","):
                item = item.strip()
                if item.isdigit():
                    idx = int(item) - 1
                    if 0 <= idx < len(self.packages):
                        indexes.append(idx)
            self.selected = [self.packages[i] for i in indexes]

        self.save()
        return self.selected

    def save(self):
        CONFIG_FILE.write_text(
            json.dumps({"packages": self.selected}, indent=4),
            encoding="utf-8",
        )

    def load(self):
        if CONFIG_FILE.exists():
            data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
            self.selected = data.get("packages", [])
        return self.selected


if __name__ == "__main__":
    manager = PackageManager()
    manager.scan()
    manager.display()
    manager.select()
  
