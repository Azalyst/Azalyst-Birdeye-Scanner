import os
import requests
import time

HELIUS_URL = "https://mainnet.helius-rpc.com "
API_KEY = os.environ.get("HELIUS_API_KEY", "")


def fetch_solana_mempool():
    """Poll Helius for large pending transactions (simplified)."""
    if not API_KEY:
        return []
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "getSignaturesForAddress",
        "params": ["Vote111111111111111111111111111111111111111", {"limit": 20}]
    }
    try:
        r = requests.post(f"{HELIUS_URL}/?api-key={API_KEY}", json=payload, timeout=10)
        data = r.json()
        return data.get("result", [])
    except Exception:
        return []
