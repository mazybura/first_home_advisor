import pickle
from pathlib import Path

from src.backend.models.user_data import UserData


class RiskClassifier:
    """Responsible for assessing a user's mortgage readiness."""

    def __init__(self, model_path: str = "src/backend/ml/model.pkl"):
        "Loading a trained ML model."
        path = Path(model_path)
        if not path.exists():
            raise FileNotFoundError(f"Model file not found at {model_path}")
        with open(path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, user_data: UserData) -> str:
        """
        Returns one of: 'ready', 'almost ready', 'not ready' based on confidence.
        """
        prob = self.predict_proba(user_data)
        if prob >= 0.8:
            return "ready"
        elif prob >= 0.5:
            return "almost ready"
        else:
            return "not ready"

    def predict_proba(self, user_data: UserData) -> float:
        """
        Returns a probability score between 0.0 and 1.0 indicating
        how confident the model is in its classification.
        """
        df = user_data.to_dataframe()
        probas = self.model.predict_proba(df)
        return float(probas[0][1])
