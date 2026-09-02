import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# ======================================================
# Test Flask routes
# ======================================================

from app import app

def test_home_page():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
""" 
def test_result_page():
    client = app.test_client()

    response = client.post(
        "/",
        data={
            "as_cm2": "10",
            "b_mm": "300",
            "e_mm": "5"
        },
        follow_redirects=True
    )

    assert response.status_code == 200
"""  

def test_result_page(monkeypatch):

    monkeypatch.setattr(
        "app.get_diameters_from_db",
        lambda: {
            "HA8": 8,
            "HA10": 10
        }
    )

    client = app.test_client()

    response = client.post(
        "/",
        data={
            "as_cm2": "10",
            "b_mm": "300",
            "e_mm": "5"
        },
        follow_redirects=True
    )

    assert response.status_code == 200