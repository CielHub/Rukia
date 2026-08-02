"""
verification_engine.py
CARRERA-HUB v2
Core Verification Engine
"""

from __future__ import annotations

import subprocess
import time


class VerificationResult:
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"


class VerificationEngine:

    def __init__(self, timeout: int = 30, interval: float = 1.0):
        self.timeout = timeout
        self.interval = interval

    def _pid(self, package: str) -> str:
        result = subprocess.run(
            ["pidof", package],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout.strip()

    def is_running(self, package: str) -> bool:
        return bool(self._pid(package))

    def wait_until_running(self, package: str):
        start = time.time()

        while time.time() - start < self.timeout:
            if self.is_running(package):
                return VerificationResult.SUCCESS
            time.sleep(self.interval)

        return VerificationResult.TIMEOUT

    def verify(self, package: str) -> dict:
        status = self.wait_until_running(package)

        return {
            "package": package,
            "status": status,
            "pid": self._pid(package),
            "timestamp": time.time(),
        }


if __name__ == "__main__":
    pkg = input("Package: ").strip()
    result = VerificationEngine().verify(pkg)
    print(result)
  
