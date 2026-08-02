"""
error_detection_engine.py
CARRERA-HUB v2
Core Error Detection Engine
"""

from __future__ import annotations

import re
import subprocess
import time


class ErrorDetectionEngine:

    DEFAULT_PATTERNS = {
        "267": re.compile(r"\b267\b"),
        "277": re.compile(r"\b277\b"),
    }

    def __init__(self):
        self.patterns = dict(self.DEFAULT_PATTERNS)

    def add_pattern(self, code: str, pattern: str):
        self.patterns[code] = re.compile(pattern)

    def read_logcat(self, lines: int = 200):
        result = subprocess.run(
            ["logcat", "-d", "-t", str(lines)],
            capture_output=True,
            text=True,
            check=False,
        )
        return result.stdout

    def detect(self):
        log = self.read_logcat()
        found = []

        for code, pattern in self.patterns.items():
            if pattern.search(log):
                found.append({
                    "error": code,
                    "timestamp": time.time(),
                })

        return found

    def has_error(self):
        return len(self.detect()) > 0


if __name__ == "__main__":
    engine = ErrorDetectionEngine()
    errors = engine.detect()

    if not errors:
        print("No supported Roblox errors detected.")
    else:
        for item in errors:
            print(item)
          
