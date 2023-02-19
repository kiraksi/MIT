# Using Bisection Search to Make the Program Faster - Write a program that uses these bounds and bisection search (for more info check out the Wikipedia page on bisection search) to find the smallest monthly payment to the cent (no more multiples of $10) such that we can pay off the debt within a year.

monthlyInterestRate = annualInterestRate / 12
minimum = balance / 12
maximum = (balance * (1 + monthlyInterestRate)**12) / 12.0

remain = balance
epsilon = 0.10

while (remain >= epsilon):
    guess = (minimum + maximum)/2

    for _ in range(12):
        newBalance = remain - guess
        monthInterest = annualInterestRate/12*newBalance
        remain = newBalance+monthInterest

    if (remain < 0):
        maximum = guess
        remain = balance

    elif (remain > epsilon):
        minimum = guess
        remain = balance

print("Lowest Payment: ", round(guess,2))
