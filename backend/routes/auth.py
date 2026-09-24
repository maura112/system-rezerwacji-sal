from flask import Blueprint, request, jsonify, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Wszystkie pola są wymagane"}), 400

    existing_user = User.query.filter_by(email=email).first()

    if existing_user:
        return jsonify({"error": "Użytkownik o tym adresie już istnieje"}), 409

    hashed_password = generate_password_hash(password)

    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Użytkownik został zarejestrowany",
        "user_id": user.id
    }), 201
@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "E-mail i hasło są wymagane"}), 400

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "Nieprawidłowy e-mail lub hasło"}), 401

    if not check_password_hash(user.password, password):
        return jsonify({"error": "Nieprawidłowy e-mail lub hasło"}), 401
    
    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_role"] = user.role

    return jsonify({
        "message": "Logowanie zakończone sukcesem!",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }
    }), 200

@auth.route("/me", methods=["GET"])
def current_user():
    if "user_id" not in session:
        return jsonify({"error": "Użytkownik nie jest zalogowany"}), 401

    return jsonify({
        "id": session["user_id"],
        "name": session["user_name"],
        "role": session["user_role"]
    }), 200

@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()

    return jsonify({
        "message": "Wylogowano"
    }), 200

