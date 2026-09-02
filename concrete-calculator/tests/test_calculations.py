import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import area_bar_cm2, compute_counts_and_spacing


# ======================================================
# Test area_bar_cm2()
# ======================================================

def test_area_bar_cm2_ha10():
    """
    Surface d'une barre HA10 :
    π * 10² / 4 / 100 = 0.7854 cm²
    """
    result = area_bar_cm2(10)

    assert round(result, 4) == 0.7854


def test_area_bar_cm2_ha20():
    """
    Surface d'une barre HA20 :
    π * 20² / 4 / 100 = 3.1416 cm²
    """
    result = area_bar_cm2(20)

    assert round(result, 4) == 3.1416


# ======================================================
# Test compute_counts_and_spacing() with monkeypatching
# ======================================================

def test_compute_counts_and_spacing_single_diameter(monkeypatch):
    """
    Vérifie le calcul pour un unique diamètre HA10.
    """

    monkeypatch.setattr(
        "app.get_diameters_from_db",
        lambda: {"HA10": 10}
    )

    results = compute_counts_and_spacing(
        as_cm2=10,
        b_mm=300,
        e_mm=5
    )

    assert len(results) == 1
    assert results[0]["name"] == "HA10"
    assert results[0]["diameter_mm"] == 10
    assert results[0]["count"] > 0
    assert results[0]["spacing_mm"] != "N/A"


def test_compute_counts_and_spacing_multiple_diameters(monkeypatch):
    """
    Vérifie que plusieurs diamètres sont correctement traités.
    """

    monkeypatch.setattr(
        "app.get_diameters_from_db",
        lambda: {
            "HA8": 8,
            "HA10": 10
        }
    )

    results = compute_counts_and_spacing(
        as_cm2=5,
        b_mm=250,
        e_mm=5
    )

    assert len(results) == 2

    names = [item["name"] for item in results]

    assert "HA8" in names
    assert "HA10" in names

    for item in results:
        assert item["count"] > 0
        assert "area_per_bar_cm2" in item
        assert "spacing_mm" in item