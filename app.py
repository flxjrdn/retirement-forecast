import streamlit as st
from datetime import date
from src.account_portfolio import AccountPortfolio, ContributionRule, WithdrawalRule
from src.interest_strategy.fixed_interest_strategy import FixedInterestStrategy

st.set_page_config(page_title="Account Portfolio Simulator", layout="wide")

st.title("📊 Account Portfolio Projection Tool")

# Sidebar for user input
st.sidebar.header("Personal Information")
birthdate = st.sidebar.date_input("Date of Birth", value=date(1990, 1, 1))

# Portfolio instance
if "portfolio" not in st.session_state or st.session_state.birthdate != birthdate:
    st.session_state.portfolio = AccountPortfolio(birthdate=birthdate)
    st.session_state.birthdate = birthdate

portfolio = st.session_state.portfolio

st.sidebar.header("Add Account")
account_name = st.sidebar.text_input("Account Name", "pension")
initial_amount = st.sidebar.number_input("Initial Amount", min_value=0.0, value=10000.0)
account_start_date = st.sidebar.date_input("Account Start Date", value=date.today())
annual_rate = st.sidebar.number_input(
    "Annual Interest Rate (e.g., 0.04 for 4%)", min_value=0.0, max_value=1.0, value=0.04
)

if st.sidebar.button("Add Account"):
    strategy = FixedInterestStrategy(annual_rate)
    try:
        portfolio.add_account(
            account_name, initial_amount, account_start_date, strategy
        )
        st.success(f"Account '{account_name}' added.")
    except ValueError as e:
        st.error(str(e))

st.sidebar.header("Add Contribution Rule")
contrib_account = st.sidebar.text_input("Account for Contribution", "pension")
contrib_amount = st.sidebar.number_input("Monthly Contribution", value=500.0)
contrib_start_age = st.sidebar.number_input("Start Age", value=30)
contrib_end_age = st.sidebar.number_input("End Age", value=65)
contrib_escalation = st.sidebar.number_input(
    "Annual Increase Rate (0.0 - 1.0)", min_value=0.0, max_value=1.0, value=0.0
)

if st.sidebar.button("Add Contribution Rule"):
    try:
        rule = ContributionRule(
            contrib_account,
            contrib_amount,
            contrib_start_age,
            contrib_end_age,
            contrib_escalation,
        )
        portfolio.add_contribution_rule(rule)
        st.success("Contribution rule added.")
    except (KeyError, ValueError) as e:
        st.error(str(e))

st.sidebar.header("Add Withdrawal Rule")
withdraw_account = st.sidebar.text_input("Account for Withdrawal", "pension")
withdraw_amount = st.sidebar.number_input("Monthly Withdrawal", value=1000.0)
withdraw_start_age = st.sidebar.number_input("Start Age for Withdrawal", value=65)
withdraw_end_age = st.sidebar.number_input("End Age for Withdrawal", value=85)

if st.sidebar.button("Add Withdrawal Rule"):
    try:
        rule = WithdrawalRule(
            withdraw_account, withdraw_amount, withdraw_start_age, withdraw_end_age
        )
        portfolio.add_withdrawal_rule(rule)
        st.success("Withdrawal rule added.")
    except (KeyError, ValueError) as e:
        st.error(str(e))

# Projection
st.header("🔄 Forecast Portfolio")
target_age = st.number_input("Target Age to Project To", min_value=0, value=70)

if st.button("Run Projection"):
    try:
        portfolio.project_to_age(target_age)
        st.success("Projection completed.")

        # Display results for each account
        total_values = []
        dates = None

        for account_name in portfolio.get_account_names():
            balance = portfolio.get_balance(account_name)
            st.metric(
                label=f"Projected Balance for {account_name}", value=f"${balance:,.2f}"
            )

            history = portfolio.account_history(account_name)
            if history:
                if dates is None:
                    dates = [d for d, _ in history]
                values = [v for _, v in history]
                if not total_values:
                    total_values = values
                else:
                    total_values = [sum(x) for x in zip(total_values, values)]

        # Show total portfolio value over time
        if dates and total_values:
            import pandas as pd

            df = pd.DataFrame({"Total Portfolio Value": total_values}, index=dates)
            st.line_chart(df)

    except Exception as e:
        st.error(f"Error during projection: {e}")
