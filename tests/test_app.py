import sys
import os

sys.path.insert(0, os.path.abspath("backend"))

import unittest
from backend.app import app


class TestSystemRezerwacji(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_strona_glowna(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_strona_logowania(self):
        response = self.client.get("/login-page")
        self.assertEqual(response.status_code, 200)

    def test_lista_sal(self):
        response = self.client.get("/rooms")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()