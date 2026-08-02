"""
recovery_engine.py
CARRERA-HUB v2
Core Recovery Engine
"""

from __future__ import annotations

import subprocess
import time
from typing import Iterable


class RecoveryEngine:

    def __init__(self, launcher=None, verifier=None,
                 force_stop_delay: float = 1.5,
                 relaunch_delay: float = 5.0):
        self.launcher = launcher
        self.verifier = verifier
        self.force_stop_delay = force_stop_delay
        self.relaunch_delay = relaunch_delay

    def force_stop(self, package: str):
        subprocess.run(
            ["am", "force-stop", package],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        time.sleep(self.force_stop_delay)

    def recover_package(self, package: str) -> dict:
        self.force_stop(package)

        if self.launcher:
            self.launcher.launch_package(package)
            time.sleep(self.relaunch_delay)
            self.launcher.open_deeplink()

        verification = None
        if self.verifier:
            verification = self.verifier.verify(package)

        return {
            "package": package,
            "action": "RECOVERY",
            "verification": verification,
            "timestamp": time.time(),
        }

    def recover_offline(self, packages: Iterable[str]):
        results = []
        for package in packages:
            results.append(self.recover_package(package))
        return results

    def recover_error(self, package: str, error_code: str):
        result = self.recover_package(package)
        result["error"] = error_code
        return result

    def handle_monitor_event(self, status: dict):
        if not status.get("alive", True):
            return self.recover_package(status["package"])
        return None

    def handle_error_event(self, event: dict):
        return self.recover_error(
            event["package"],
            event["error"],
        )


if __name__ == "__main__":
    print("RecoveryEngine is intended to be used by main.py")
  
