"""
private_server_manager.py
CARRERA-HUB v2
Core Private Server Manager
"""

from __future__ import annotations

import json
import re
from pathlib import Path

CONFIG_FILE = Path("private_server.json")


class PrivateServerManager:

    def __init__(self):
        self.private_server_link = ""
        self.deeplink = ""

    def validate(self, link: str) -> bool:
        return bool(re.search(r"(roblox\.com|www\.roblox\.com).*(privateServerLinkCode|code=)", link))

    def convert_to_deeplink(self, link: str) -> str:
        place = re.search(r"placeId=(\d+)", link)
        code = re.search(r"(?:privateServerLinkCode|code)=([A-Za-z0-9_-]+)", link)

        if not (place and code):
            raise ValueError("Invalid private server link.")

        place_id = place.group(1)
        access_code = code.group(1)

        return (
            f"roblox://placeID={place_id}"
            f"&linkCode={access_code}"
        )

    def save(self, link: str):
        if not self.validate(link):
            raise ValueError("Unsupported Roblox private server link.")

        self.private_server_link = link
        self.deeplink = self.convert_to_deeplink(link)

        CONFIG_FILE.write_text(
            json.dumps(
                {
                    "private_server_link": self.private_server_link,
                    "deeplink": self.deeplink,
                },
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(self):
        if not CONFIG_FILE.exists():
            return None

        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        self.private_server_link = data.get("private_server_link", "")
        self.deeplink = data.get("deeplink", "")
        return data

    def show(self):
        print("\n=== Private Server ===")
        print("Link     :", self.private_server_link or "-")
        print("Deeplink :", self.deeplink or "-")


if __name__ == "__main__":
    manager = PrivateServerManager()
    link = input("Paste Private Server Link: ").strip()
    manager.save(link)
    manager.show()
  
