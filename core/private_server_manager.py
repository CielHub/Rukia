"""
private_server_manager.py
CARRERA-HUB v2
Bug Fix #2
"""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

CONFIG_FILE = Path("private_server.json")


class PrivateServerManager:

    def __init__(self):
        self.private_server_link = ""
        self.deeplink = ""

    def validate(self, link: str) -> bool:
        host = urlparse(link).netloc.lower()
        return "roblox.com" in host or "ro.blox.com" in host

    def extract(self, link: str):
        parsed = urlparse(link)
        query = parse_qs(parsed.query)

        code = query.get("code", [None])[0] or query.get("privateServerLinkCode", [None])[0]
        place_id = query.get("placeId", [None])[0]

        if not code:
            raise ValueError("Private Server code not found.")

        return code, place_id

    def convert_to_deeplink(self, link: str) -> str:
        code, place_id = self.extract(link)

        if place_id:
            return f"roblox://placeID={place_id}&linkCode={code}"

        return f"roblox://navigation/share_links?code={code}&type=Server"

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
                    "format": "share_links" if "share?" in link else "legacy",
                },
                indent=4,
            ),
            encoding="utf-8",
        )

    def load(self):
        if not CONFIG_FILE.exists():
            return None

        data = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        self.private_server_link = data.get("private_server_link","")
        self.deeplink = data.get("deeplink","")
        return data
        
