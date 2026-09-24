from flask import Blueprint, request, jsonify, session
from models import db, Reservation, Room

reservations = Blueprint("reservations", __name__)


@reservations.route("/reservations", methods=["POST"])
def create_reservation():

    if "user_id" not in session:
        return jsonify({
            "error": "Musisz być zalogowany"
        }), 401

    data = request.get_json()

    room_id = data.get("room_id")
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")

    if not room_id or not date or not start_time or not end_time:
        return jsonify({
            "error": "Wszystkie pola są wymagane"
        }), 400

    room = Room.query.get(room_id)

    if not room:
        return jsonify({
            "error": "Sala nie istnieje"
        }), 404

    if start_time >= end_time:
        return jsonify({
            "error": "Godzina zakończenia musi być późniejsza niż rozpoczęcia"
        }), 400

    conflict = Reservation.query.filter(
        Reservation.room_id == room_id,
        Reservation.date == date,
        Reservation.start_time < end_time,
        Reservation.end_time > start_time
    ).first()

    if conflict:
        return jsonify({
            "error": "Sala jest już zarezerwowana w tym terminie"
        }), 409

    reservation = Reservation(
        user_id=session["user_id"],
        room_id=room_id,
        date=date,
        start_time=start_time,
        end_time=end_time
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "message": "Rezerwacja została utworzona",
        "reservation_id": reservation.id
    }), 201


@reservations.route("/reservations", methods=["GET"])
def get_my_reservations():

    if "user_id" not in session:
        return jsonify({
            "error": "Musisz być zalogowany"
        }), 401

    reservations_list = Reservation.query.filter_by(
        user_id=session["user_id"]
    ).all()

    result = []

    for reservation in reservations_list:

        room = Room.query.get(reservation.room_id)

        result.append({
            "id": reservation.id,
            "room": room.name if room else "Nieznana",
            "building": room.building if room else "Nieznany",
            "date": reservation.date,
            "start_time": reservation.start_time,
            "end_time": reservation.end_time
        })

    return jsonify(result), 200


@reservations.route("/reservations/<int:reservation_id>", methods=["DELETE"])
def cancel_reservation(reservation_id):

    if "user_id" not in session:
        return jsonify({
            "error": "Musisz być zalogowany"
        }), 401

    reservation = Reservation.query.get(reservation_id)

    if not reservation:
        return jsonify({
            "error": "Rezerwacja nie istnieje"
        }), 404

    if reservation.user_id != session["user_id"]:
        return jsonify({
            "error": "Nie możesz anulować tej rezerwacji"
        }), 403

    db.session.delete(reservation)
    db.session.commit()

    return jsonify({
        "message": "Rezerwacja została anulowana"
    }), 200
@reservations.route("/rooms/search", methods=["GET"])
def search_rooms():

    query = Room.query

    building = request.args.get("building")
    min_capacity = request.args.get("min_capacity")
    equipment = request.args.get("equipment")

    if building:
        query = query.filter(Room.building.ilike(f"%{building}%"))

    if min_capacity:
        try:
            min_capacity = int(min_capacity)
            query = query.filter(Room.capacity >= min_capacity)
        except ValueError:
            return jsonify({
                "error": "Nieprawidłowa pojemność"
            }), 400

    rooms = query.all()

    result = []

    for room in rooms:

        if equipment:
            room_equipment = room.equipment.lower()
            if equipment.lower() not in room_equipment:
                continue

        result.append({
            "id": room.id,
            "name": room.name,
            "building": room.building,
            "floor": room.floor,
            "capacity": room.capacity,
            "equipment": room.equipment,
            "status": room.status
        })

    return jsonify(result), 200

@reservations.route("/rooms/<int:room_id>/schedule", methods=["GET"])
def room_schedule(room_id):

    date = request.args.get("date")

    if not date:
        return jsonify({
            "error": "Data jest wymagana"
        }), 400

    room = Room.query.get(room_id)

    if not room:
        return jsonify({
            "error": "Sala nie istnieje"
        }), 404

    reservations_list = Reservation.query.filter_by(
        room_id=room_id,
        date=date
    ).all()

    result = []

    for reservation in reservations_list:
        result.append({
            "start_time": reservation.start_time,
            "end_time": reservation.end_time
        })

    return jsonify({
        "room": room.name,
        "building": room.building,
        "date": date,
        "reservations": result
    }), 200
@reservations.route("/all-reservations", methods=["GET"])
def all_reservations():
    reservations_list = Reservation.query.order_by(
        Reservation.date,
        Reservation.start_time
    ).all()

    result = []

    for reservation in reservations_list:
        room = Room.query.get(reservation.room_id)

        result.append({
            "room": room.name,
            "building": room.building,
            "date": reservation.date,
            "start_time": reservation.start_time,
            "end_time": reservation.end_time
        })

    return jsonify(result), 200