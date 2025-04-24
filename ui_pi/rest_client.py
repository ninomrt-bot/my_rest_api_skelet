"""
Client simple pour l’API REST (backend_api) hébergée
dans le conteneur Portainer (réseau OT).
"""
import requests, json, time
from pathlib import Path
from config import API_BASE_URL, OF_CACHE_PATH

TIMEOUT = 4    # secondes

# ------------------------------------------------------------------ #
def can_connect_to_rest() -> bool:
    try:
        r = requests.get(f"{API_BASE_URL}/test", timeout=TIMEOUT)
        return r.status_code == 200
    except Exception:
        return False

# ------------------------------------------------------------------ #
def get_of_list() -> list[dict]:
    """
    Retourne une liste :
    [{'numero':.., 'code':.., 'quantite':.., 'etat':..}, ...]
    """
    r = requests.get(f"{API_BASE_URL}/orders", timeout=TIMEOUT)
    r.raise_for_status()
    return r.json().get("orders", [])

# ------------------------------------------------------------------ #
def get_of_components(of_numero: str) -> list[str]:
    r = requests.get(
        f"{API_BASE_URL}/orders/components",
        params={"of_name": of_numero},
        timeout=TIMEOUT
    )
    r.raise_for_status()
    return r.json().get("components", [])

# ------------------------------------------------------------------ #
def add_manual_of(numero, code, quantite) -> bool:
    payload = {"numero": numero, "code": code, "quantite": quantite}
    r = requests.post(f"{API_BASE_URL}/orders", json=payload, timeout=TIMEOUT)
    return r.status_code in (200, 201)

# ------------------------------------------------------------------ #
# ---  Gestion du cache local (mode dégradé) ------------------------ #
def _save_cache(lst):
    OF_CACHE_PATH.write_text(json.dumps(lst, ensure_ascii=False, indent=2))

def _load_cache() -> list:
    if OF_CACHE_PATH.exists():
        return json.loads(OF_CACHE_PATH.read_text())
    return []

def get_of_list_cached() -> list[dict]:
    try:
        data = get_of_list()
        if data:
            _save_cache(data)
            return data
    except Exception as e:
        print(f"[REST] get_of_list_cached error: {e}")
    return _load_cache()
