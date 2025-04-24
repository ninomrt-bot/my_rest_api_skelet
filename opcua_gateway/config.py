# opcua_gateway/config.py

# Where your REST API lives (the “api” service in docker-compose)
REST_URL = "http://backend_api:5000/api"

# OPC‑UA endpoint (listen on all interfaces in the container)
OPCUA_ENDPOINT = "opc.tcp://0.0.0.0:4840"

# A URI for your namespace—can be anything unique
NAMESPACE_URI = "http://nee.local/opcua"

# Map the REST keys to OPC‑UA node names
NODE_MAPPINGS = {
    "numero":   "OF_Number",
    "code":     "ProductCode",
    "quantite": "Quantity",
    "etat":     "State"
}

# How often to poll your REST API (seconds)
POLL_SECONDS = 2

# (Optional) a friendly name your server will advertise
SERVER_NAME = "NEE202504 OPC-UA Gateway"
# opcua_gateway/config.py

# Adresse de ton API REST (nom du service dans docker-compose)
REST_URL = "http://api:5000/api"

# Endpoint OPC-UA exposé par ce container (écoute sur toutes les interfaces)
OPCUA_ENDPOINT = "opc.tcp://0.0.0.0:4840"

# URI unique pour ton namespace OPC-UA
NAMESPACE_URI = "http://nee.local/opcua"

# Mappage des clés JSON de l’API REST vers les noms de variables OPC-UA
NODE_MAPPINGS = {
    "numero":   "OF_Number",
    "code":     "ProductCode",
    "quantite": "Quantity",
    "etat":     "State"
}

# Fréquence de polling de l’API REST (en secondes)
POLL_SECONDS = 2

# Nom convivial que ton serveur OPC-UA affichera
SERVER_NAME = "NEE202504 OPC-UA Gateway"
