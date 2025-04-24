# opcua_gateway/gateway.py

import asyncio, requests, time
from asyncua import ua, Server
import config as cfg

async def init_opcua_server() -> tuple[Server, dict]:
    server = Server()
    await server.init()
    # **DO NOT** await set_endpoint()—it’s synchronous
    server.set_endpoint(cfg.OPCUA_ENDPOINT)
    server.set_server_name(cfg.SERVER_NAME)

    # Limit to NO security so we don’t need certs/keys
    server.set_security_policy([ua.SecurityPolicyType.NoSecurity])

    idx     = await server.register_namespace(cfg.NAMESPACE_URI)
    objects = server.nodes.objects

    # Dynamically create one variable per REST field
    nodes = {}
    for rest_key, node_name in cfg.NODE_MAPPINGS.items():
        var = await objects.add_variable(idx, node_name, "")
        await var.set_writable()
        nodes[rest_key] = var

    return server, nodes

def fetch_current_of() -> dict | None:
    try:
        resp = requests.get(f"{cfg.REST_URL}/orders", timeout=5)
        resp.raise_for_status()
        data = resp.json().get("orders", [])
        return data[0] if data else None
    except Exception as e:
        print(f"⚠️ REST error: {e}")
        return None

async def main_loop():
    server, nodes = await init_opcua_server()
    async with server:
        print(f"✅ OPC UA server listening on {cfg.OPCUA_ENDPOINT}")
        while True:
            of = fetch_current_of()
            if of:
                for key, var in nodes.items():
                    val = of.get(key, "")
                    await var.write_value(val)
            await asyncio.sleep(cfg.POLL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main_loop())
