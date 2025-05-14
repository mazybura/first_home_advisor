import sys
from pathlib import Path


sys.path.append(str(Path(__file__).resolve().parents[1]))  # FIXME: Try without sys.path

import streamlit as st
from backend.models.user_data import UserData
from backend.services.app_controller import AppController


def render_app():
    """
    Renders UI.
    Allows users to input personal and financial data,
    and displays their mortgage readiness assessment.
    """
    st.set_page_config(page_title="FirstHome Advisor", layout="centered")
    st.title("🏡 FirstHome Advisor")
    st.markdown(
        "Check your financial readiness to buy your first home with a mortgage."
    )

    with st.form("user_input_form"):
        age: int = st.slider("Age", 18, 100, 30)
        employment_type: str = st.selectbox(
            "Employment Type", ["permanent", "freelance", "business"]
        )
        monthly_income: float = st.number_input(
            "Gross Monthly Income (PLN)", min_value=0.0, step=500.0
        )
        monthly_expenses: float = st.number_input(
            "Monthly Living Expenses (PLN)", min_value=0.0, step=100.0
        )
        existing_loans: float = st.number_input(
            "Monthly Loan Repayments (PLN)", min_value=0.0, step=100.0
        )
        own_contribution: float = st.number_input(
            "Own Contribution / Down Payment (PLN)", min_value=0.0, step=1000.0
        )
        property_value: float = st.number_input(
            "Planned Property Value (PLN)", min_value=0.0, step=1000.0
        )
        dependents: int = st.number_input(
            "Number of Financial Dependents", min_value=0, step=1
        )

        submitted: bool = st.form_submit_button("Check Mortgage Readiness")

    if submitted:
        try:
            user_data = UserData(
                age=age,
                employment_type=employment_type,
                monthly_income=monthly_income,
                monthly_expenses=monthly_expenses,
                existing_loans=existing_loans,
                own_contribution=own_contribution,
                property_value=property_value,
                dependents=dependents,
            )

            controller = AppController()
            result = controller.assess_user(user_data)

            st.success(f"**Assessment Result:** {result['category'].capitalize()}")
            st.metric("📊 Debt-to-Income Ratio (DTI)", f"{result['dti']:.2f}")
            st.metric("💰 Estimated Maximum Loan", f"{result['max_credit']:.0f} PLN")
            st.metric("🔎 Model Confidence", f"{result['confidence'] * 100:.1f} %")

            st.subheader("📝 Personalized Recommendations:")
            for rec in result["recommendations"]:
                st.write(f"- {rec}")

        except Exception as e:
            st.error(f"❌ Input validation error: {e}")


if __name__ == "__main__":
    render_app()
