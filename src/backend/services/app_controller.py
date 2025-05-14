from src.backend.models.user_data import UserData
from src.backend.services.credit_calculator import CreditCalculator
from src.backend.services.risk_classifier import RiskClassifier


class AppController:
    def __init__(self):
        self.calculator = CreditCalculator()
        self.classifier = RiskClassifier()

    def assess_user(self, user_data: UserData) -> dict:
        dti = self.calculator.calculate_dti(user_data)
        credit = self.calculator.calculate_max_credit(user_data)
        category = self.classifier.predict(user_data)
        confidence = self.classifier.predict_proba(user_data)
        recommendations = self.calculator.recommendations(user_data)

        return {
            "dti": dti,
            "max_credit": credit,
            "category": category,
            "confidence": confidence,
            "recommendations": recommendations,
        }
