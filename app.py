import logging
from flask import Flask, request, jsonify
import sqlite3
import os

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

# In-memory storage for quick lookup
users = {}

# Database setup
DB_FILE = "amf_users.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            site_code TEXT NOT NULL,
            imsi TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_user_db(user_id, name, site_code, imsi):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (user_id, name, site_code, imsi)
        VALUES (?, ?, ?, ?)
    ''', (user_id, name, site_code, imsi))
    conn.commit()
    conn.close()

@app.route('/amf/register', methods=['POST'])
def register_user():
    try:
        data = request.get_json(silent=True)

        if not data:
            logging.error("AMF: No data provided for registration")
            return jsonify({"error": "No data provided"}), 400

        user_id = data.get("user_id")
        name = data.get("name")
        site_code = data.get("site_code")
        imsi = data.get("imsi")

        if not user_id or not name or not site_code or not imsi:
            logging.error("AMF: Missing registration information")
            return jsonify({"error": "Missing registration information"}), 400

        if not imsi.startswith("12345"):
            logging.warning(f"AMF: IMSI {imsi} is not allowed to access the network")
            return jsonify({"error": "Access denied: invalid IMSI"}), 403

        if user_id in users:
            logging.warning(f"AMF: User {user_id} is already registered")
            return jsonify({"error": "User already registered"}), 400

        # Save in memory and in database
        users[user_id] = {"name": name, "site_code": site_code, "imsi": imsi}
        insert_user_db(user_id, name, site_code, imsi)

        logging.info(f"AMF: User {user_id} registered successfully with IMSI {imsi}")
        return jsonify({"message": f"User {user_id} registered successfully"}), 201

    except Exception as e:
        logging.error(f"Error registering user: {e}")
        return jsonify({"error": str(e)}), 400

@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200

@app.route('/amf/users', methods=['GET'])
def get_users():
    try:
        return jsonify({"users": users}), 200
    except Exception as e:
        logging.error(f"Error retrieving users: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=83)

