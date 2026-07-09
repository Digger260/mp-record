#!/usr/bin/env python3
"""
Generate a links-only directory page for every current UK MP, using the
official UK Parliament Members API (https://members-api.parliament.uk/).

Usage:
    pip install requests
    python scripts/fetch_mps.py            # only creates missing files
    python scripts/fetch_mps.py --refresh  # regenerates every file from the API
"""

import re
import sys
import time
from pathlib import Path

import requests

API = "https://members-api.parliament.uk/api"
OUT_DIR = Path(__file__).resolve().parent.parent / "_mps"


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def fetch_all_current_mps():
    skip, take = 0, 20
    while True:
        r = requests.get(
            f"{API}/Members/Search",
            params={"House": 1, "IsCurrentMember": "true", "skip": skip, "take": take},
            timeout=30,
        )
        r.raise_for_status()
        items = r.json().get("items", [])
        if not items:
            break
        for item in items:
            yield item["value"]
        skip += take
        time.sleep(0.2)  # be polite to the API


def render(mp: dict) -> str:
    mp_id = mp["id"]
    name = mp["nameDisplayAs"]
    ipsa = name.lower()
    for h in ("rt hon ", "sir ", "dame ", "dr ", "mr ", "mrs ", "ms ", "miss "):
        if ipsa.startswith(h):
            ipsa = ipsa[len(h):]
    ipsa = re.sub(r"[^a-z0-9]+", "-", ipsa).strip("-")
    party = (mp.get("latestParty") or {}).get("name", "")
    membership = mp.get("latestHouseMembership") or {}
    constituency = membership.get("membershipFrom", "")
    since = (membership.get("membershipStartDate") or "")[:10]

    return f"""---
name: "{name}"
party: "{party}"
constituency: "{constituency}"
mp_since: "{since}"
parliament_id: {mp_id}
ipsa_slug: "{ipsa}"
---
"""


def main():
    refresh = "--refresh" in sys.argv
    OUT_DIR.mkdir(exist_ok=True)
    created = skipped = 0
    for mp in fetch_all_current_mps():
        path = OUT_DIR / f"{slugify(mp['nameDisplayAs'])}.md"
        if path.exists() and not refresh:
            skipped += 1
            continue
        path.write_text(render(mp), encoding="utf-8")
        created += 1
        print(f"wrote {path.name}")
    print(f"\nDone: {created} written, {skipped} skipped (use --refresh to regenerate all).")


if __name__ == "__main__":
    main()
