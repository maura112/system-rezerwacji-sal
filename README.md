# System rezerwacji sal

System rezerwacji sal na uczelni wykonany w ramach projektu JEE.

## Technologie

- Python
- Flask
- HTML
- CSS
- JavaScript
- SQLite
- SQLAlchemy
- Docker
- unittest
- Git / GitHub

## Funkcjonalności

### Użytkownik

- rejestracja
- logowanie i wylogowanie
- przeglądanie dostępnych sal
- wyszukiwanie sal według:
  - budynku
  - minimalnej pojemności
  - wyposażenia
- sprawdzanie kalendarza zajętości sal
- tworzenie rezerwacji
- przeglądanie własnych rezerwacji
- anulowanie rezerwacji

### Administrator

Administrator posiada dodatkowe uprawnienia:

- dodawanie sal
- usuwanie sal
- zarządzanie dostępnymi salami
- dostęp do panelu administratora

## Struktura projektu

```text
system-rezerwacji-sal/
│
├── backend/
│   ├── app.py
│   ├── models.py
│   └── routes/
│       ├── auth.py
│       ├── rooms.py
│       └── reservations.py
│
├── frontend/
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── rooms.html
│   ├── reservation.html
│   ├── reservations.html
│   ├── search.html
│   ├── calendar.html
│   └── admin.html
│
├── tests/
│   └── test_app.py
│
├── instance/
│   └── database.db
│
├── Dockerfile
├── requirements.txt
├── .gitignore
└── README.md