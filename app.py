import streamlit as st
from datetime import date
from src.account_portfolio import AccountPortfolio, ContributionRule, WithdrawalRule
from src.interest_strategy.fixed_interest_strategy import FixedInterestStrategy

st.set_page_config(page_title="Account Portfolio Simulator", layout="wide")

st.title("📊 Account Portfolio Projection Tool")

# Sidebar for user input
st.sidebar.header("Personal Information")
birthdate = st.sidebar.date_input("Date of Birth", value=date(1990, 1, 1))

# Session state persistence
if "portfolio" not in st.session_state or st.session_state.birthdate != birthdate:
    st.session_state.portfolio = AccountPortfolio(birthdate=birthdate)
    st.session_state.birthdate = birthdate

portfolio = st.session_state.portfolio

# Add account section
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

# Show and manage accounts
if portfolio.get_account_names():
    st.subheader("📅 Accounts")
    for name in portfolio.get_account_names():
        col1, col2 = st.columns([4, 1])
        with col1:
            balance = portfolio.get_balance(name)
            account = portfolio._accounts[name]
            st.write(f"**{name}**")
            st.write(f"- Balance: ${balance:,.2f}")
            st.write(f"- Start Date: {account.current_date().strftime('%Y-%m-%d')}")
            st.write(
                f"- Annual Interest Rate: {((1 + account._strategy.get_monthly_rate(date.today()))**12 - 1)*100:.2f}%"
            )
        with col2:
            if st.button("Delete", key=f"del_{name}"):
                del portfolio._accounts[name]
                st.rerun()

# Add contribution rule section
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

# Show and manage contribution rules
if portfolio._contribution_rules:
    st.subheader("💸 Contribution Rules")
    for i, rule in enumerate(portfolio._contribution_rules):
        with st.expander(f"Edit Contribution Rule {i+1}"):
            account = st.text_input(
                f"Account {i}", value=rule.account_name, key=f"ca_{i}"
            )
            amount = st.number_input(f"Amount {i}", value=rule.amount, key=f"am_{i}")
            start_age = st.number_input(
                f"Start Age {i}", value=rule.start_age, key=f"sa_{i}"
            )
            end_age = st.number_input(f"End Age {i}", value=rule.end_age, key=f"ea_{i}")
            escalation = st.number_input(
                f"Annual Increase {i}",
                min_value=0.0,
                max_value=1.0,
                value=rule.annual_increase_rate,
                key=f"es_{i}",
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_cr_{i}"):
                    try:
                        portfolio._contribution_rules[i] = ContributionRule(
                            account, amount, start_age, end_age, escalation
                        )
                        st.success("Updated successfully")
                    except Exception as e:
                        st.error(str(e))
            with col2:
                if st.button("Delete", key=f"delete_cr_{i}"):
                    del portfolio._contribution_rules[i]
                    st.rerun()

# Add withdrawal rule section
st.sidebar.header("Add Withdrawal Rule")
withdraw_account = st.sidebar.text_input("Account for Withdrawal", "pension")
withdraw_amount = st.sidebar.number_input("Monthly Withdrawal", value=1000.0)
withdraw_start_age = st.sidebar.number_input("Start Age for Withdrawal", value=65)
withdraw_end_age = st.sidebar.number_input("End Age for Withdrawal", value=100)

if st.sidebar.button("Add Withdrawal Rule"):
    try:
        rule = WithdrawalRule(
            withdraw_account, withdraw_amount, withdraw_start_age, withdraw_end_age
        )
        portfolio.add_withdrawal_rule(rule)
        st.success("Withdrawal rule added.")
    except (KeyError, ValueError) as e:
        st.error(str(e))

# Show and manage withdrawal rules
if portfolio._withdrawal_rules:
    st.subheader("📉 Withdrawal Rules")
    for i, rule in enumerate(portfolio._withdrawal_rules):
        with st.expander(f"Edit Withdrawal Rule {i+1}"):
            account = st.text_input(
                f"WAccount {i}", value=rule.account_name, key=f"wa_{i}"
            )
            amount = st.number_input(f"WAmount {i}", value=rule.amount, key=f"wam_{i}")
            start_age = st.number_input(
                f"WStart Age {i}", value=rule.start_age, key=f"wsa_{i}"
            )
            end_age = st.number_input(
                f"WEnd Age {i}", value=rule.end_age, key=f"wea_{i}"
            )
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Update", key=f"update_wr_{i}"):
                    try:
                        portfolio._withdrawal_rules[i] = WithdrawalRule(
                            account, amount, start_age, end_age
                        )
                        st.success("Updated successfully")
                    except Exception as e:
                        st.error(str(e))
            with col2:
                if st.button("Delete", key=f"delete_wr_{i}"):
                    del portfolio._withdrawal_rules[i]
                    st.rerun()

# Projection
st.header("🔄 Forecast Portfolio")
target_age = st.number_input("Target Age to Project To", min_value=0, value=100)

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
