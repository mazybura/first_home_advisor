from src.backend.models.user_data import UserData


class CreditCalculator:
    """
    Provides utility methods for calculating debt-to-income ratio,
    estimating maximum credit capacity, and generating financial recommendations
    based on user financial data.
    """

    def calculate_dti(self, user_data: UserData) -> float:
        """
        Calculates the user's Debt-to-Income ratio.
        DTI is defined as the ratio of monthly expenses and existing loans
        to the user's monthly income. If the income is zero, returns infinity.
        """
        if user_data.monthly_income == 0:
            return float("inf")
        return (
            user_data.monthly_expenses + user_data.existing_loans
        ) / user_data.monthly_income

    def calculate_max_credit(self, user_data: UserData) -> float:
        """
        Estimates the maximum credit amount the user can afford.
        This is a simplified formula that assumes the user can allocate
        all disposable income (income - expenses) to loan repayments,
        multiplied by a fixed factor.
        """
        return (user_data.monthly_income - user_data.monthly_expenses) * 100

    def recommendations(self, user_data: UserData) -> list[str]:
        """
        Generates a list of personalized financial recommendations
        based on the user's contribution, expenses, and existing loans.
        """
        recs = []
        if user_data.own_contribution < 0.1 * user_data.property_value:
            recs.append("Try to increase your own contribution")
        if user_data.monthly_expenses > 0.5 * user_data.monthly_income:
            recs.append("Try to reduce your monthly expenses")
        if user_data.existing_loans > 0:
            recs.append("Consider repaying existing loans to improve your score")
        if not recs:
            recs.append("You're on the right track!")
        return recs
