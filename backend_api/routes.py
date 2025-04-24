from flask import Blueprint, jsonify, request
import odoo_client as oc

api_routes = Blueprint("api_routes", __name__)

# ------------------------------------------------------------------ #
@api_routes.route("/test", methods=["GET"])
def test():
    return jsonify({"message": "Hello from the NEE202504 API REST!"})

# ------------------------------------------------------------------ #
@api_routes.route("/orders", methods=["GET"])
def list_orders():
    """Renvoie la liste des OF (avec cache)."""
    orders = oc.get_of_list_cached()
    return jsonify({"orders": orders})

# ------------------------------------------------------------------ #
@api_routes.route("/orders/components", methods=["GET"])
def list_components():
    """/orders/components?of_name=WH/MO/00012"""
    of_name = request.args.get("of_name")
    if not of_name:
        return jsonify({"error": "paramètre of_name manquant"}), 400
    comps = oc.get_of_components(of_name)
    return jsonify({"components": comps})
