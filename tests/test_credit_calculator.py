import pytest

from src.backend.models.user_data import UserData
from src.backend.services.credit_calculator import CreditCalculator


@pytest.fixture
def user_data():
    return UserData(
        age=30,
        employment_type="permanent",
        monthly_income=5000,
        monthly_expenses=1500,
        existing_loans=500,
        own_contribution=20000,
        property_value=300000,
        dependents=1,
    )


@pytest.fixture
def calculator():
    return CreditCalculator()


def test_calculate_dti(user_data, calculator):
    dti = calculator.calculate_dti(user_data)
    expected = (1500 + 500) / 5000
    assert pytest.approx(dti, 0.001) == expected


def test_calculate_max_credit(user_data, calculator):
    max_credit = calculator.calculate_max_credit(user_data)
    expected = (5000 - 1500) * 100
    assert max_credit == expected


def test_recommendations_are_list(user_data, calculator):
    recs = calculator.recommendations(user_data)
    assert isinstance(recs, list)
    assert len(recs) > 0
