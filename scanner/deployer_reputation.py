import json
import os
import time
from datetime import datetime, timezone

import requests

CACHE_FILE = "data/scam_cache.json"
RUGCHECK_API = "https://api.rugcheck.xyz "


def _load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}


def _save_cache(cache):
    os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


def refresh_scam_cache():
    """Pull latest scam data from public lists."""
    cache = _load_cache()
    try:
        resp = requests.get(f"{RUGCHECK_API}/v1/stats/new", timeout=15)
        if resp.ok:
            for entry in resp.json().get("recent", []):
                addr = entry.get("token") or entry.get("mint")
                if addr:
                    cache[addr] = {
                        "type": entry.get("type", "rugpull"),
                        "last_seen": datetime.now(timezone.utc).isoformat()
                    }
    except Exception:
        pass
    _save_cache(cache)
    return cache


def check_deployer(chain: str, token_address: str) -> dict:
    """Return scam_flag and reasons for a token."""
    cache = refresh_scam_cache()
    addr = token_address.lower()
    result = {"scam_flag": 0, "scam_reasons": []}
    if addr in cache:
        result["scam_flag"] = 1
        result["scam_reasons"].append(f"known_{cache[addr]['type']}")
    return result
