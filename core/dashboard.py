"""
dashboard.py
CARRERA-HUB v2
Core Dashboard
"""

from __future__ import annotations

import os
import time


class Dashboard:

    def __init__(self):
        self.runtime_started = time.time()

    def clear(self):
        os.system("clear")

    def _uptime(self):
        sec = int(time.time() - self.runtime_started)
        h, rem = divmod(sec, 3600)
        m, s = divmod(rem, 60)
        return f"{h:02}:{m:02}:{s:02}"

    def render(self, package_status):
        self.clear()

        print("╔══════════════════════════════════════════════════════════════════════╗")
        print("║                         CARRERA-HUB v2                             ║")
        print("╠══════════════════════════════════════════════════════════════════════╣")
        print(f"║ Runtime Uptime : {self._uptime():<49}║")
        print(f"║ Loaded Packages: {len(package_status):<49}║")
        print("╠════╦══════════════════════════════╦══════════════╦═══════════════════╣")
        print("║ No ║ Package                      ║ Status       ║ Last Error        ║")
        print("╠════╬══════════════════════════════╬══════════════╬═══════════════════╣")

        if not package_status:
            print("║ -- ║ No package loaded            ║ -            ║ -                 ║")
        else:
            for idx, item in enumerate(package_status, 1):
                pkg = item.get("package","-")[:28]
                status = item.get("status","UNKNOWN")[:12]
                error = item.get("error","-")[:17]
                print(f"║ {idx:<2} ║ {pkg:<28} ║ {status:<12} ║ {error:<17} ║")

        print("╚════╩══════════════════════════════╩══════════════╩═══════════════════╝")

    def loop(self, provider, interval=2):
        try:
            while True:
                self.render(provider())
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nDashboard stopped.")


if __name__ == "__main__":
    demo = [
        {"package":"com.roblox.clienu","status":"ONLINE","error":"-"},
        {"package":"com.roblox.clienv","status":"RECOVERING","error":"267"},
    ]
    Dashboard().render(demo)

