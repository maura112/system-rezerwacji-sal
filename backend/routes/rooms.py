from flask import Blueprint, request, jsonify, session
from models import db, Room

rooms = Blueprint("rooms", __name__)


def is_admin():
    return session.get("user_role") == "admin"


@rooms.route("/rooms", methods=["GET"])
def get_rooms():

    rooms_list = Room.query.all()

    return jsonify([
        {
            "id": room.id,
            "name": room.name,
            "building": room.building,
            "floor": room.floor,
            "capacity": room.capacity,
            "equipment": room.equipment,
            "status": room.status
        }
        for room in rooms_list
    ]), 200


@rooms.route("/rooms", methods=["POST"])
def add_room():

    if not is_admin():
        return jsonify({
            "error": "Brak uprawnień administratora"
        }), 403

    data = request.get_json()

    name = data.get("name")
    building = data.get("building")
    floor = data.get("floor")
    capacity = data.get("capacity")
    equipment = data.get("equipment", "")
    status = data.get("status", "dostępna")

    if not name or not building or floor is None or capacity is None:
        return jsonify({
            "error": "Nazwa, budynek, piętro i pojemność są wymagane"
        }), 400

    room = Room(
        name=name,
        building=building,
        floor=floor,
        capacity=capacity,
        equipment=equipment,
        status=status
    )

    db.session.add(room)
    db.session.commit()

    return jsonify({
        "message": "Sala została dodana",
        "room_id": room.id
    }), 201



@rooms.route("/rooms/<int:room_id>", methods=["DELETE"])
def delete_room(room_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Musisz być zalogowany"
        }), 401

    if session.get("user_role") != "admin":
        return jsonify({
            "error": "Brak uprawnień"
        }), 403

    room = Room.query.get(room_id)

    if not room:
        return jsonify({
            "error": "Sala nie istnieje"
        }), 404

    db.session.delete(room)
    db.session.commit()

    return jsonify({
        "message": "Sala została usunięta"
    }), 200