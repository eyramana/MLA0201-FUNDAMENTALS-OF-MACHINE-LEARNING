"""
Unit tests for recommendations.py
"""

from recommendations import get_recommendations, DISEASE_RECOMMENDATIONS, DEFAULT_RECOMMENDATION

def test_get_recommendations_known_disease():
    key = "Tomato___Early_blight"
    res = get_recommendations(key)
    assert res["disease_name"] == "Tomato Early Blight"
    assert res["crop"] == "Tomato"
    assert len(res["organic_control"]) > 0
    assert len(res["chemical_control"]) > 0

def test_get_recommendations_unknown_disease():
    key = "NonExistent_Disease_123"
    res = get_recommendations(key)
    assert res == DEFAULT_RECOMMENDATION
    assert "Unspecified" in res["disease_name"]
