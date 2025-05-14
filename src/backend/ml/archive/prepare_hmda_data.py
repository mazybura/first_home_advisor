import pandas as pd
import os

INPUT_FILE = "src/backend/ml/2023_public_lar_csv.csv"
OUTPUT_FILE = "src/backend/ml/cleaned_hmda_data.csv"
CHUNKSIZE = 100_000


def age_to_int(age_val: float | int | str) -> int | None:
    """Convert numeric or string age to integer (handles edge cases)."""
    try:
        return int(age_val)
    except:
        return None


def process_chunk(chunk: pd.DataFrame) -> pd.DataFrame:
    """Process a chunk of the HMDA dataset into the UserData format."""
    required_cols = [
        "applicant_age",
        "income",
        "loan_amount",
        "property_value",
        "action_taken",
    ]

    chunk = chunk[required_cols].copy()
    # Konwersja kolumn liczbowych na float
    chunk["income"] = pd.to_numeric(chunk["income"], errors="coerce")
    chunk["loan_amount"] = pd.to_numeric(chunk["loan_amount"], errors="coerce")
    chunk["property_value"] = pd.to_numeric(chunk["property_value"], errors="coerce")
    chunk = chunk.dropna()
    chunk = chunk[chunk["action_taken"].isin([1, 3])]

    # Convert income from thousands to PLN/month (assuming $1k = ~4000 PLN for realism)
    chunk["income"] = pd.to_numeric(chunk["income"], errors="coerce")
    chunk["monthly_income"] = chunk["income"] * 4000 / 12

    chunk["own_contribution"] = chunk["property_value"] - chunk["loan_amount"]
    chunk["monthly_expenses"] = chunk["monthly_income"] * 0.3
    chunk["existing_loans"] = 0
    chunk["dependents"] = 0
    chunk["employment_type"] = "permanent"
    chunk["target"] = chunk["action_taken"].map({1: 1, 3: 0})
    chunk["age"] = chunk["applicant_age"].apply(age_to_int)

    chunk = chunk[
        (chunk["monthly_income"] > 0)
        & (chunk["own_contribution"] >= 0)
        & (chunk["age"].notnull())
    ]

    final_cols = [
        "age",
        "employment_type",
        "monthly_income",
        "monthly_expenses",
        "existing_loans",
        "own_contribution",
        "property_value",
        "dependents",
        "target",
    ]
    return chunk[final_cols]


def main() -> None:
    if not os.path.exists(INPUT_FILE):
        print(f"❌ File not found: {INPUT_FILE}")
        return

    first_chunk = True
    total_rows = 0

    print("🚀 Starting data processing...")
    for chunk in pd.read_csv(INPUT_FILE, chunksize=CHUNKSIZE, low_memory=False):
        chunk.columns = chunk.columns.str.strip()
        processed = process_chunk(chunk)
        total_rows += len(processed)

        processed.to_csv(
            OUTPUT_FILE,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )
        first_chunk = False
        print(f"✅ Processed chunk, total rows so far: {total_rows}")

    print(f"\n🎉 Done! Cleaned data saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
