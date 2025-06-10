def estimate_life_expectancy(age, gender, lifestyle_score) -> int:
    base = 80 if gender == "male" else 84
    adj = int((lifestyle_score - 5) * 1.5)  # crude modifier
    return int(min(100, max(age + 1, base + adj)))


def project_financials(
    current_age,
    retirement_age,
    savings,
    monthly_savings,
    monthly_expenses,
    life_expectancy,
    growth_rate=0.05,
):
    years_to_retire = retirement_age - current_age
    years_post_retirement = life_expectancy - retirement_age

    # Pre-retirement accumulation
    total_savings = savings
    for _ in range(years_to_retire):
        total_savings = (total_savings + monthly_savings * 12) * (1 + growth_rate)

    # Post-retirement depletion
    balance = total_savings
    drawdown = []
    for _ in range(years_post_retirement):
        balance = (balance - monthly_expenses * 12) * (1 + growth_rate)
        drawdown.append(balance)

    return total_savings, drawdown
