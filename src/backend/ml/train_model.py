import pandas as pd
import pickle
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer


# DATA_PATH = Path("src/backend/ml/cleaned_hmda_data.csv") # USA
DATA_PATH = Path("src/backend/ml/pl_mortgage_training_data.csv")
MODEL_PATH = Path("src/backend/ml/model.pkl")


def load_data() -> tuple[pd.DataFrame, pd.Series]:
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["target"])
    y = df["target"]
    return X, y


def train_model():
    X, y = load_data()

    # Check class distribution
    print("[DEBUG] class distribution:")  # TODO: Add logger
    print(y.value_counts(normalize=True))

    # Preprocessing
    categorical = ["employment_type"]
    numeric = [col for col in X.columns if col not in categorical]

    numeric_transformer = SimpleImputer(strategy="mean")
    categorical_transformer = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )

    preprocessor = ColumnTransformer(
        [
            ("num", numeric_transformer, numeric),
            ("cat", categorical_transformer, categorical),
        ]
    )

    clf = Pipeline(
        [
            ("preprocessor", preprocessor),
            ("classifier", RandomForestClassifier(n_estimators=100, random_state=42)),
        ]
    )

    # Train
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    clf.fit(X_train, y_train)

    # Save model
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(clf, f)

    print("Model trained and saved to:", MODEL_PATH)


if __name__ == "__main__":
    train_model()
