import math
import argparse
import sys


def calc_nominal_interest(interest):
    return (interest / 100) / 12

# -------------------------------------------------------------------------------------------
def calc_number_of_monthly_payments(type, principal, payment, interest):
    if type == "annuity":
        # calculate number of monthly payments
        i = calc_nominal_interest(interest)

        # calculate number of months:
        n = math.log((payment / (payment - i * principal)), 1 + i)

        # round up the total from above then convert to years + months
        n = math.ceil(n)
        years = n / 12
        months = n % 12

        # if number of months is greater than 12 months (1 yr)
        if n > 12:
            print(f"It will take {math.ceil(years) if months > 11 else math.floor(years)} years "
                  f"and {months} months to repay this loan!")
        elif n == 12:
            print(f"It will take 1 year to repay this loan")
        else:
            print(f"It will take {months} months to repay this loan!")

        overpayment_total = (math.ceil(payment) * n) - principal
        print(overpayment_total)


# -------------------------------------------------------------------------------------------
def calc_annuity_payment(type, principal, periods, interest):
    if type == "annuity":
        # calculate interest
        i = calc_nominal_interest(interest)

        # calculate monthly payment
        x = math.pow(1 + i, periods)
        monthly_payment = principal * ((i * x) / (x - 1))

        print(f"Your annuity payment = {math.ceil(monthly_payment)}!")

        overpayment_total = (math.ceil(monthly_payment) * periods) - principal
        print(f"Overpayment = {overpayment_total}")


# -------------------------------------------------------------------------------------------
def calc_loan_principal(type, payment, periods, interest):
    if type == "annuity":
        i = calc_nominal_interest(interest)

        x = math.pow(1 + i, periods)

        principal = payment / ((i * x) / (x - 1))

        print(f"Your loan principal = {math.floor(principal)}!")

        overpayment_total = (math.ceil(payment) * periods) - principal
        print(f"Overpayment = {math.ceil(overpayment_total)}")


# -------------------------------------------------------------------------------------------
def calc_differentiated_payments(type, principal, periods, interest):
    if type == "diff":
        i = calc_nominal_interest(interest)

        m = 1
        total = 0

        while m <= periods:
            diff = math.ceil(principal / periods + i * (principal - (principal * (m - 1) / periods)))
            total += diff

            print(f"Month {m}: payment is {diff}")
            m += 1

        overpayment_total = total - principal
        print(f"\nOverpayment =  {math.ceil(overpayment_total)}")


# -------------------------------------------------------------------------------------------
# allow for int or float type
def int_or_float(value):
    try:
        return int(value)
    except ValueError:
        return float(value)


parser = argparse.ArgumentParser(description='Calculate missing parameter')
parser.add_argument('--payment', type=int_or_float, help='payment amount for loan')
parser.add_argument('--principal', type=int_or_float, help='principal amount for loan')
parser.add_argument('--periods', type=int_or_float, help='number of months needed to repay the loan')
parser.add_argument('--interest', type=int_or_float, help='annual interest')
parser.add_argument('--type', type=str, help='choose between annuity or diff')

args = parser.parse_args()


# -------------------------------------------------------------------------------------------
def main():
    if len(sys.argv) < 5:  # Check for 5 required arguments plus the script name
        print("Incorrect parameters")
        return

    # check existence of required args
    if (args.type is None
            or args.interest is None
            or args.interest < 0
            or any(value is not None and value < 0 for value in [args.principal, args.payment, args.periods])):
        print("Incorrect parameters")
        return

    # check those of type "annuity"
    if args.type == "annuity":
        if args.periods is None:
            calc_number_of_monthly_payments(args.type, args.principal, args.payment, args.interest)
        elif args.payment is None:
            calc_annuity_payment(args.type, args.principal, args.periods, args.interest)
        elif args.principal is None:
            calc_loan_principal(args.type, args.payment, args.periods, args.interest)
        else:
            print("Incorrect parameters")

    # check type "diff"
    elif args.type == "diff":
        if args.payment is None:
            calc_differentiated_payments(args.type, args.principal, args.periods, args.interest)
        else:
            print("Incorrect parameters")

    else:
        print("Incorrect parameters")


# -------------------------------------------------------------------------------------------
# run program
if __name__ == "__main__":
    main()
