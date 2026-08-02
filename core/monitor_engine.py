"""
monitor_engine.py
CARRERA-HUB v2
Core Monitor Engine
"""

from __future__ import annotations

import subprocess
import threading
import time


class MonitorEngine:

    def __init__(self, interval: float = 5.0):
        self.interval = interval
        self.packages = []
        self.running = False
        self.callback = None
        self._thread = None

    def set_packages(self, packages):
        self.packages = list(packages)

    def set_callback(self, callback):
        self.callback = callback

    def is_running(self, package: str) -> bool:
        result = subprocess.run(
            ["pidof", package],
            capture_output=True,
            text=True,
            check=False,
        )
        return bool(result.stdout.strip())

    def check_once(self):
        report = []

        for package in self.packages:
            alive = self.is_running(package)

            status = {
                "package": package,
                "alive": alive,
                "timestamp": time.time(),
            }

            report.append(status)

            if self.callback:
                self.callback(status)

        return report

    def _loop(self):
        while self.running:
            self.check_once()
            time.sleep(self.interval)

    def start(self):
        if self.running:
            return

        self.running = True
        self._thread = threading.Thread(
            target=self._loop,
            daemon=True,
        )
        self._thread.start()

    def stop(self):
        self.running = False

    def join(self):
        if self._thread:
            self._thread.join(timeout=2)


if __name__ == "__main__":
    monitor = MonitorEngine()
    monitor.set_packages([
        input("Package: ").strip()
    ])

    monitor.set_callback(print)
    monitor.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        monitor.stop()
        monitor.join()
      
