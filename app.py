from flask import Flask, request, jsonify
from flask_cors import CORS
from database import create_connection, create_tables, hash_password, check_password

app = Flask(__name__)

CORS(app)

create_tables()


@app.route("/")
def home():
    return "Tamkini Backend is running!"


@app.route("/api/register", methods=["POST"])
def register():

    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({
            "success": False,
            "message": "All fields are required"
        }), 400

    hashed_password = hash_password(password)

    conn = create_connection()
    cursor = conn.cursor()

    try:

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password)
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Account created successfully"
        }), 201

    except Exception:

        return jsonify({
            "success": False,
            "message": "Email already exists"
        }), 409

    finally:

        conn.close()


@app.route("/api/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "success": False,
            "message": "Username and password are required"
        }), 400

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email, password FROM users WHERE name = ? OR email = ?",
        (username, username)
    )

    user = cursor.fetchone()

    conn.close()

    if user is None:

        return jsonify({
            "success": False,
            "message": "Invalid username or password"
        }), 401

    user_id, name, user_email, hashed_password = user

    if check_password(password, hashed_password):

        return jsonify({
            "success": True,
            "message": "Login successful",
            "user": {
                "id": user_id,
                "name": name,
                "email": user_email
            }
        })

    return jsonify({
        "success": False,
        "message": "Invalid username or password"
    }), 401


if __name__ == "__main__":
    app.run(debug=True)