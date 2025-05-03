from src.backend.models.user_data import UserData


class RiskClassifier:
    """Responsible for assessing a user's mortgage readiness."""

    def __init__(self):
        pass

    def predict(self, user_data: UserData) -> str:
        """
        Predicts the user's mortgage readiness category.
        Returns a predicted category label, e.g., "ready", "not ready".
        """
        return "ready"

    def predict_proba(self, user_data: UserData) -> float:
        """
        Returns a probability score between 0.0 and 1.0 indicating
        how confident the model is in its classification.
        """
        return 0.85
