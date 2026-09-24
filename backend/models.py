from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False, default="student")


class Room(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(50), nullable=False)

    building = db.Column(db.String(100), nullable=False)

    floor = db.Column(db.Integer, nullable=False)

    capacity = db.Column(db.Integer, nullable=False)

    equipment = db.Column(db.String(255), nullable=True)

    status = db.Column(db.String(30), nullable=False, default="dostępna")

class Reservation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    room_id = db.Column(
        db.Integer,
        db.ForeignKey("room.id"),
        nullable=False
    )

    date = db.Column(db.String(10), nullable=False)

    start_time = db.Column(db.String(5), nullable=False)

    end_time = db.Column(db.String(5), nullable=False)
    