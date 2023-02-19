# Paying Debt off in a Year - Write a program to calculate the credit card balance after one year if a person only pays the minimum monthly payment required by the credit card company each month. For each month, calculate statements on the monthly payment and remaining balance. At the end of 12 months, print out the remaining balance. 

for _ in range(12):
    minimum_payment = balance * monthlyPaymentRate
    unpaid_balance = balance - minimum_payment
    interest = (annualInterestRate/12.0) * unpaid_balance
    balance = unpaid_balance + interest

print("Remaining balance: ",round(balance, 2))
