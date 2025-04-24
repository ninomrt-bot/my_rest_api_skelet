import os
from flask import Flask
from routes import api_routes
from dotenv import load_dotenv

load_dotenv()                       # charge .env si présent

app = Flask(__name__)
app.register_blueprint(api_routes, url_prefix="/api")

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV", "production") != "production"
    app.run(host="0.0.0.0", port=5000, debug=debug)
