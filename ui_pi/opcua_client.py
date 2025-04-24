"""
Client *mono‑shot* qui pousse l’OF sélectionné vers le serveur OPC‑UA.
Le conteneur « gateway » expose le serveur à OPCUA_ENDPOINT.
"""
from asyncua import Client
import asyncio
from config import OPCUA_ENDPOINT

NODES = {          
    "numero"  : "OF_Numero",
    "code"    : "OF_Code",
    "quantite": "OF_Qte",
    "etat"    : "OF_Etat"
}

async def _envoi_async(of: dict):
    async with Client(OPCUA_ENDPOINT) as cli:
        root = cli.nodes.objects
        for k, node_name in NODES.items():
            try:
                node = await root.get_child(node_name)
                await node.write_value(of.get(k, ""))
            except Exception as e:
                print(f"[OPC] write {node_name} failed: {e}")

def envoyer_of(of: dict):
    """
    Appelé depuis pilotage_app :
    envoyer_of({"numero":"WH/MO/00012", "code": "...", …})
    """
    asyncio.run(_envoi_async(of))
