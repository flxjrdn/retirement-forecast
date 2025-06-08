import streamlit as st
from calculations import estimate_life_expectancy, project_financials
import matplotlib.pyplot as plt

st.title("Retirement & Life Expectancy Planner")

# Inputs
age = st.slider("Current Age", 20, 70, 35)
gender = st.radio("Gender", ["male", "female"])
retirement_age = st.slider("Planned Retirement Age", 40, 75, 65)
savings = st.number_input("Current Savings ($)", value=50000)
monthly_savings = st.number_input("Monthly Savings ($)", value=500)
monthly_expenses = st.number_input("Expected Monthly Expenses ($)", value=3000)
lifestyle_score = st.slider("Lifestyle Score (1 = poor, 10 = excellent)", 1, 10, 6)

# Calculation
life_expectancy = estimate_life_expectancy(age, gender, lifestyle_score)
total_savings, drawdown = project_financials(age, int(retirement_age), savings, monthly_savings, monthly_expenses, int(life_expectancy))

# Outputs
st.write(f"📈 **Estimated Life Expectancy:** {life_expectancy} years")
st.write(f"💰 **Savings at Retirement:** ${total_savings:,.0f}")
st.write("📉 Projected Savings After Retirement:")

# Plot
fig, ax = plt.subplots()
ax.plot(range(retirement_age, life_expectancy), drawdown, label="Savings Balance")
ax.axhline(0, color="red", linestyle="--")
ax.set_xlabel("Age")
ax.set_ylabel("Balance ($)")
ax.legend()
st.pyplot(fig)