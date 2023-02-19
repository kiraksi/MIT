# Paying Debt Off in a Year - Now write a program that calculates the minimum fixed monthly payment needed in order pay off a credit card balance within 12 months. By a fixed monthly payment, we mean a single number which does not change each month, but instead is a constant amount that will be paid each month.

monthly_interest = annualInterestRate/12.0
minimum_fixed = 0

while True:
    minimum_fixed += 10
    updated_balance = balance

    for _ in range(12):
        monthly_unpaid = updated_balance - minimum_fixed
        updated_balance = monthly_unpaid + (monthly_interest * monthly_unpaid)
    
    if updated_balance <= 0:
        break

print("Lowest Payment: ", minimum_fixed)
