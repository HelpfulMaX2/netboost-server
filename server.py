from flask import Flask, request, send_file, abort
from io import BytesIO
import os
import hmac

app = Flask(__name__)
MARIME = 10 * 1024 * 1024
DATE_TEST = os.urandom(MARIME)
TOKEN = os.environ.get("NETBOOST_TOKEN", "")

@app.route("/")
def index():
    return {"server": "NetBoost", "status": "online", "version": "1.0"}

@app.route("/info")
def info():
    return {"size": MARIME, "filename": "test.bin", "range_supported": True}

@app.route("/download")
def download():
    cheie = request.headers.get("X-NetBoost-Token", "")
    if not TOKEN or not hmac.compare_digest(cheie, TOKEN):
        abort(403)
    return send_file(BytesIO(DATE_TEST), mimetype="application/octet-stream",
                     as_attachment=True, download_name="test.bin",
                     conditional=True, max_age=0)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
