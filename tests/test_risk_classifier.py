from src.backend.models.user_data import UserData
from src.backend.services.risk_classifier import RiskClassifier


def test_predict_returns_string():
    user = UserData(30, "permanent", 5000, 1500, 500, 20000, 300000, 1)
    clf = RiskClassifier()
    result = clf.predict(user)
    assert isinstance(result, str)


def test_predict_proba_in_range():
    user = UserData(30, "permanent", 5000, 1500, 500, 20000, 300000, 1)
    clf = RiskClassifier()
    proba = clf.predict_proba(user)
    assert isinstance(proba, float)
    assert 0.0 <= proba <= 1.0
