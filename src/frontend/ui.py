import sys
from pathlib import Path
from typing import Literal

from PIL import Image

sys.path.append(str(Path(__file__).resolve().parents[1]))
import streamlit as st

from backend.models.user_data import UserData
from backend.services.app_controller import AppController


def flag_switcher():
    def get_flag_html(code: str, current: str) -> str:
        border = "3px solid #4CAF50" if code == current else "1px solid #ccc"
        box_shadow = "0 0 6px rgba(0,0,0,0.3)" if code == current else "none"
        return (
            f"<a href='?lang={code}' target='_self'>"
            f"<img src='https://flagcdn.com/w40/{code}.png' "
            f"style='width: 40px; margin: 0 5px; cursor: pointer; border: {border}; box-shadow: {box_shadow}; border-radius: 6px;'>"
            f"</a>"
        )

    col1, col2, col3 = st.columns([9, 1, 1])
    with col2:
        st.markdown(get_flag_html("pl", st.session_state.lang), unsafe_allow_html=True)
    with col3:
        st.markdown(get_flag_html("gb", st.session_state.lang), unsafe_allow_html=True)


Lang = Literal["pl", "gb"]

st.set_page_config(page_title="FirstHome Advisor", layout="centered")

if "lang" not in st.session_state:
    st.session_state.lang = st.query_params.get("lang", "pl")
flag_switcher()


lang = st.session_state.lang


flag_pl = Image.open("src/frontend/assets/flag_pl.png")
flag_en = Image.open("src/frontend/assets/flag_gb.png")


translations = {
    "pl": {
        "title": "🏡 FirstHome Advisor",
        "subtitle": "Oceń swoją gotowość do zakupu pierwszego mieszkania na kredyt.",
        "form_button": "Sprawdź zdolność",
        "age": "Wiek",
        "income": "Miesięczny dochód brutto (PLN)",
        "expenses": "Miesięczne wydatki (PLN)",
        "loans": "Raty istniejących kredytów (PLN)",
        "contribution": "Wkład własny (PLN)",
        "value": "Wartość nieruchomości (PLN)",
        "dependents": "Liczba osób na utrzymaniu",
        "employment": "Forma zatrudnienia",
        "result": "Wynik oceny",
        "dti": "📊 Wskaźnik DTI",
        "credit": "💰 Maksymalny kredyt",
        "confidence": "🔎 Pewność modelu",
        "recommendations": "📝 Rekomendacje",
    },
    "gb": {
        "title": "🏡 FirstHome Advisor",
        "subtitle": "Check your financial readiness to buy your first home with a mortgage.",
        "form_button": "Check Mortgage Readiness",
        "age": "Age",
        "income": "Gross Monthly Income (PLN)",
        "expenses": "Monthly Expenses (PLN)",
        "loans": "Monthly Loan Repayments (PLN)",
        "contribution": "Own Contribution (PLN)",
        "value": "Planned Property Value (PLN)",
        "dependents": "Number of Financial Dependents",
        "employment": "Employment Type",
        "result": "Assessment Result",
        "dti": "📊 Debt-to-Income Ratio",
        "credit": "💰 Estimated Maximum Loan",
        "confidence": "🔎 Model Confidence",
        "recommendations": "📝 Personalized Recommendations",
    },
}

recommendation_translations = {
    "pl": {
        "You're on the right track!": "Jesteś na dobrej drodze!",
        "Try to increase your own contribution": "Spróbuj zwiększyć wkład własny",
        "Try to reduce your monthly expenses": "Spróbuj zmniejszyć miesięczne wydatki",
        "Consider repaying existing loans to improve your score": "Rozważ spłatę istniejących zobowiązań, aby poprawić wynik",
    },
    "en": {
        "You're on the right track!": "You're on the right track!",
        "Try to increase your own contribution": "Try to increase your own contribution",
        "Try to reduce your monthly expenses": "Try to reduce your monthly expenses",
        "Consider repaying existing loans to improve your score": "Consider repaying existing loans to improve your score",
    },
}

employment_labels = {
    "pl": {
        "permanent": "Na etacie",
        "freelance": "Freelancer",
        "business": "Działalność gospodarcza",
    },
    "gb": {
        "permanent": "Permanent",
        "freelance": "Freelance",
        "business": "Business",
    },
}


def t(key: str, lang: Lang) -> str:
    return translations[lang].get(key, key)


lang = st.session_state.lang


st.title(t("title", lang))
st.markdown(t("subtitle", lang))


with st.form("user_input_form"):
    age = st.slider(t("age", lang), 18, 100, 30)
    employment_options = ["permanent", "freelance", "business"]
    employment_type = st.selectbox(
        t("employment", lang),
        options=employment_options,
        format_func=lambda val: employment_labels[lang][val],
    )
    monthly_income = st.number_input(t("income", lang), min_value=0.0, step=500.0)
    monthly_expenses = st.number_input(t("expenses", lang), min_value=0.0, step=100.0)
    existing_loans = st.number_input(t("loans", lang), min_value=0.0, step=100.0)
    own_contribution = st.number_input(
        t("contribution", lang), min_value=0.0, step=1000.0
    )
    property_value = st.number_input(t("value", lang), min_value=0.0, step=1000.0)
    dependents = st.number_input(t("dependents", lang), min_value=0, step=1)

    submitted = st.form_submit_button(t("form_button", lang))


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

        st.success(f"**{t('result', lang)}:** {result['category'].capitalize()}")
        st.metric(t("dti", lang), f"{result['dti']:.2f}")
        st.metric(t("credit", lang), f"{result['max_credit']:.0f} PLN")
        st.metric(t("confidence", lang), f"{result['confidence'] * 100:.1f} %")
        st.subheader(t("recommendations", lang))
        for rec in result["recommendations"]:
            translated = recommendation_translations[lang].get(rec, rec)
            st.write(f"- {translated}")

    except Exception as e:
        st.error(f"❌ Input validation error: {e}")
