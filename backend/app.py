from flask import Flask, send_from_directory, session
from flask_cors import CORS
from models import db
from routes.auth import auth
from routes.rooms import rooms
from routes.reservations import reservations


app = Flask(__name__)

app.config["SECRET_KEY"] = "super-tajny-klucz-systemu-rezerwacji"

CORS(app, supports_credentials=True)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(auth)
app.register_blueprint(rooms)
app.register_blueprint(reservations)



@app.route("/login-page")
def login_page():
    return send_from_directory("../frontend", "login.html")

@app.route("/dashboard")
def dashboard():
    return send_from_directory("../frontend", "dashboard.html")

@app.route("/register-page")
def register_page():
    return send_from_directory("../frontend", "register.html")

@app.route("/rooms-page")
def rooms_page():
    return send_from_directory("../frontend", "rooms.html")

@app.route("/reservation-page")
def reservation_page():
    return send_from_directory("../frontend", "reservation.html")

@app.route("/reservations-page")
def reservations_page():
    return send_from_directory("../frontend", "reservations.html")

@app.route("/search-page")
def search_page():
    return send_from_directory("../frontend", "search.html")

@app.route("/calendar-page")
def calendar_page():
    return send_from_directory("../frontend", "calendar.html")

@app.route("/occupancy-page")
def occupancy_page():
    return send_from_directory("../frontend", "occupancy.html")

@app.route("/admin-page")
def admin_page():

    if "user_id" not in session:
        return "Musisz być zalogowany", 401

    if session.get("user_role") != "admin":
        return "Brak uprawnień", 403

    return send_from_directory("../frontend", "admin.html")



@app.route("/")
def home():
    return send_from_directory("../frontend", "index.html")

@app.route("/health")
def health():
    try:
        db.session.execute(db.text("SELECT 1"))
        return {
            "status": "ok",
            "database": "ok"
        }, 200
    except Exception as e:
        return {
            "status": "error",
            "database": "error"
        }, 500


with app.app_context():
    db.create_all()

    from models import Room

    if Room.query.count() == 0:
        rooms_data = [
            Room(
                name="101",
                building="Budynek A",
                floor=1,
                capacity=30,
                equipment="Projektor, komputer, tablica",
                status="dostępna"
            ),
            Room(
                name="102",
                building="Budynek A",
                floor=1,
                capacity=20,
                equipment="Projektor, tablica",
                status="dostępna"
            ),
            Room(
                name="201",
                building="Budynek B",
                floor=2,
                capacity=50,
                equipment="Projektor, nagłośnienie, komputer",
                status="dostępna"
            ),
            Room(
                name="202",
                building="Budynek B",
                floor=2,
                capacity=15,
                equipment="Komputer, tablica",
                status="dostępna"
            )
        ]

        db.session.add_all(rooms_data)
        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)