"""
private_server_manager.py
CARRERA-HUB v2
Bug Fix #1
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CONFIG_FILE = Path("private_server.json")


class PrivateServerManager:

    def __init__(self):
        self.private_server_link = ""
        self.deeplink = ""

    def validate(self, link: str) -> bool:
        return (
            "roblox.com" in link.lower()
            and ("share?" in link.lower() or "privateserverlinkcode" in link.lower())
        )

    def extract(self, link: str):
        parsed = urlparse(link)
        query = parse_qs(parsed.query)

        code = (
            query.get("privateServerLinkCode", [None])[0]
            or query.get("code", [None])[0]
        )

        place_id = query.get("placeId", [None])[0]

        return {
            "code": code,
            "place_id": place_id,
        }

    def convert_to_deeplink(self, link: str) -> str:
        data = self.extract(link)

        if not data["code"]:
            raise ValueError("Private Server code not found.")

        # New Roblox share links often do not expose placeId.
        # Save a temporary deeplink containing only the link code.
        if data["place_id"]:
            return (
                f"roblox://placeID={data['place_id']}"
                f"&linkCode={data['code']}"
            )

        return f"roblox://navigation/join?linkCode={data['code']}"

    def save(self, link: str):
        if not self.validate(link):
            raise ValueError("Unsupported Roblox link.")

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
        print("\nPrivate Server Link :", self.private_server_link or "-")
        print("Generated Deeplink  :", self.deeplink or "-")


if __name__ == "__main__":
    manager = PrivateServerManager()
    manager.save(input("Private Server Link: ").strip())
    manager.show()
    
