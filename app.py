"""
Khal — Serveur Web Flask
"""

from flask import Flask, render_template, request, jsonify, session
from khal_core import Khal
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# Instance globale de Khal
khal = Khal()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message vide"}), 400

    resultat = khal.repondre(message)
    return jsonify(resultat)


@app.route("/historique", methods=["GET"])
def historique():
    return jsonify({"historique": khal.get_historique()})


@app.route("/reset", methods=["POST"])
def reset():
    khal.memoire.effacer()
    return jsonify({"status": "ok", "message": "Mémoire effacée."})


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "status": "online",
        "version": Khal.VERSION,
        "messages": khal.stats["messages_recus"],
        "duree": khal.memoire.duree_session()
    })


if __name__ == "__main__":
    print("\n" + "="*50)
    print("  🤖 KHAL — Intelligence Artificielle Générale")
    print("="*50)
    print("  → Serveur démarré sur http://localhost:5000")
    print("  → Ctrl+C pour arrêter")
    print("="*50 + "\n")
    app.run(debug=True, port=5000)
