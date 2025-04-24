import xmlrpc.client, json, os, time
from pathlib import Path
from config import ODOO_URL, ODOO_DB, ODOO_USER, ODOO_PASS, CACHE_PATH

# ------------------------------------------------------------------ #
# 1) Connexion                                                       #
# ------------------------------------------------------------------ #
def _connect():
    common  = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
    uid     = common.authenticate(ODOO_DB, ODOO_USER, ODOO_PASS, {})
    models  = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
    return uid, models

# ------------------------------------------------------------------ #
# 2) Lecture nomenclature (code BOM)                                 #
# ------------------------------------------------------------------ #
def _get_bom_code(bom_id: int) -> str | None:
    uid, models = _connect()
    res = models.execute_kw(
        ODOO_DB, uid, ODOO_PASS,
        'mrp.bom', 'read',
        [bom_id],
        {'fields': ['code']}
    )
    return res[0].get('code') if res else None

# ------------------------------------------------------------------ #
# 3) Liste des OF (confirmés)                                        #
# ------------------------------------------------------------------ #
def get_of_list() -> list[dict]:
    uid, models = _connect()

    ofs = models.execute_kw(
        ODOO_DB, uid, ODOO_PASS,
        'mrp.production', 'search_read',
        [[['state', 'in', ['confirmed', 'cancel']]]],          # filtre simple
        {'fields': ['name', 'product_id', 'product_qty', 'state', 'bom_id'],
         'limit': 100}
    )

    resultat = []
    for of in ofs:
        nom_article = of['product_id'][1] if of['product_id'] else "Article ?"
        code_bom    = _get_bom_code(of['bom_id'][0]) if of.get('bom_id') else None
        code        = f"{nom_article} ({code_bom or '?'})"

        resultat.append({
            "numero":   of['name'],
            "code":     code,
            "quantite": of['product_qty'],
            "etat":     of['state']
        })
    return resultat

# ------------------------------------------------------------------ #
# 4) Composants d’un OF                                              #
# ------------------------------------------------------------------ #
def get_of_components(of_name: str) -> list[str]:
    uid, models = _connect()

    rec = models.execute_kw(
        ODOO_DB, uid, ODOO_PASS,
        'mrp.production', 'search_read',
        [[['name', '=', of_name]]],
        {'fields': ['move_raw_ids'], 'limit': 1}
    )
    if not rec:
        return [f"OF '{of_name}' introuvable"]

    move_ids = rec[0]['move_raw_ids']
    if not move_ids:
        return ["Aucun composant"]

    moves = models.execute_kw(
        ODOO_DB, uid, ODOO_PASS,
        'stock.move', 'read',
        [move_ids],
        {'fields': ['product_id', 'product_uom_qty']}
    )
    return [
        f"{mv['product_id'][1]} x{mv['product_uom_qty']}"
        for mv in moves
    ]

# ------------------------------------------------------------------ #
# 5) Cache local JSON : write / read                                 #
# ------------------------------------------------------------------ #
def _save_cache(data: list):
    try:
        Path(CACHE_PATH).write_text(json.dumps(data, indent=2), encoding="utf-8")
    except Exception as e:
        print(f"⚠️  save_cache: {e}")

def _load_cache() -> list:
    try:
        return json.loads(Path(CACHE_PATH).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"⚠️  load_cache: {e}")
        return []

# ------------------------------------------------------------------ #
# 6) Version « avec cache »                                          #
# ------------------------------------------------------------------ #
def get_of_list_cached() -> list[dict]:
    try:
        data = get_of_list()
        _save_cache(data)
        return data
    except Exception as e:
        print(f"⚠️  Odoo KO → cache : {e}")
        return _load_cache()
