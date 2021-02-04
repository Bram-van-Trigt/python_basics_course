#Problem set 1
#Part A: House Hunting

#total_cost                     = price of dream home
#portion_down_payment           = 0.25 of total_cost
#current_savings                = 0 at start
#current_savings*r/12           = intrest from saving each month
#r                              = annual return rate 0.04(4%)
#portion_saved                  = variable percentage to saving from monthly salary
#monthly salary                 = annual salary/12
#semi_annual_raise              = decimal percentage of semi annual raise
#downpayment within 36 months


starting_annual_salary = int(input("Enter your starting annual salary:"))
semi_annual_raise = 0.07
total_cost = 1000000
portion_of_downpayment = total_cost*0.25
current_savings = 0                             #start with no savings
r = 0.04                                        #intrest rate of 4% on savings
months = 0
semi_annual_raise_months = 0
epsilon = 100                                   #100 dollar afwijking toegestaan
low = 0                                         #lowest monthly saving
high = 10000
guess = (high+low)//2

num_guesses = 0

while (current_savings < (portion_of_downpayment - epsilon) or current_savings > (portion_of_downpayment + epsilon)) and ((high -1 ) > low):
    current_savings = 0
    annual_salary = starting_annual_salary
    monthly_salary = annual_salary/12
    while months < 36:
        decimal_guess = guess/10000
        current_savings = (current_savings + ((current_savings * r) / 12)) + (monthly_salary * decimal_guess)
        months += 1
        semi_annual_raise_months += 1
        if semi_annual_raise_months == 6:
            annual_salary = annual_salary * (1 + semi_annual_raise)
            monthly_salary = annual_salary / 12
            semi_annual_raise_months = 0
    if current_savings <(portion_of_downpayment - epsilon):
        low = guess
    else:
        high = guess
    num_guesses +=1
    guess = (high+low)//2
    months = 0
    semi_annual_raise_months = 0
if (high-1) <= low:
    print("It is not possible to pay the downpayment in three years.")
else:
    print("entered starting salary:", starting_annual_salary)
    print("portion to save:", decimal_guess)
    print("Number of guesses:", num_guesses)