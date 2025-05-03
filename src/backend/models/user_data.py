from pydantic import BaseModel, Field, field_validator
import pandas as pd


class UserData(BaseModel):
    """
    Represents a user's personal and financial information,
    used for mortgage readiness assessment.

    Attributes:
        age: Age of the user.
        employment_type: Type of employment (e.g., "permanent", "freelance").
        monthly_income: Gross monthly income.
        monthly_expenses: Monthly living expenses.
        existing_loans: Total monthly loan repayments.
        own_contribution: User's own contribution (down payment).
        property_value: Value of the intended property.
        dependents: Number of financial dependents.
    """

    age: int = Field(..., ge=18, le=100, description="Age must be between 18 and 100")
    employment_type: str
    monthly_income: float = Field(..., ge=0)
    monthly_expenses: float = Field(..., ge=0)
    existing_loans: float = Field(..., ge=0)
    own_contribution: float = Field(..., ge=0)
    property_value: float = Field(..., ge=0)
    dependents: int = Field(..., ge=0)

    @field_validator("employment_type")
    @classmethod
    def validate_employment_type(cls, v: str) -> str:
        allowed = {"permanent", "freelance", "business"}
        if v not in allowed:
            raise ValueError(f"employment_type must be one of {allowed}")
        return v

    def to_dataframe(self) -> pd.DataFrame:
        """
        Converts the user data into a single-row Df,
        formatted for machine learning input and further processing.
        """
        return pd.DataFrame([self.model_dump()])
