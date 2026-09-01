import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import get_db_connection, get_diameters_from_db

def test_postgres_connection():
    conn = get_db_connection()

    assert conn is not None

    conn.close()


def test_diameters_loaded():

    diameters = get_diameters_from_db()

    assert "HA8" in diameters
    assert diameters["HA8"] == 8

    assert "HA10" in diameters
    assert diameters["HA10"] == 10

    assert "HA20" in diameters
    assert diameters["HA20"] == 20