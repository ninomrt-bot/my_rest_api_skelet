"""
Paramètres de connexion Odoo (Équipe C)
→ surchargeables via variables d’environnement.
"""
import os

ODOO_URL  = os.getenv("ODOO_URL",  "http://10.10.0.10:9060")
ODOO_DB   = os.getenv("ODOO_DB",   "NEE")
ODOO_USER = os.getenv("ODOO_USER", "OperateurC@nee.com")
ODOO_PASS = os.getenv("ODOO_PASS", "nee25Codoo!")

# Fichier JSON pour le cache local des OF
CACHE_PATH = os.getenv("OF_CACHE_PATH", "/tmp/of_cache.json")
