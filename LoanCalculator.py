import math
import argparse
import sys

def calculate_number_of_payments(principal, payment, interest):
    i = interest / (12 * 100)
    n = math.log(payment / (payment - i * principal), 1 + i)
    return math.ceil(n)

def calculate_annuity_payment(principal, periods, interest):
    i = interest / (12 * 100)
    payment = principal * (i * (1 + i) ** periods) / ((1 + i) ** periods - 1)
    return math.ceil(payment)

def calculate_loan_principal(payment, periods, interest):
    i = interest / (12 * 100)
    principal = payment / ((i * (1 + i) ** periods) / ((1 + i) ** periods - 1))
    return round(principal)

def convert_months_to_years_and_months(months):
    years = months // 12
    remaining_months = months % 12
    if years == 0:
        return f"{remaining_months} month{'s' if remaining_months > 1 else ''}"
    elif remaining_months == 0:
        return f"{years} year{'s' if years > 1 else ''}"
    else:
        return f"{years} year{'s' if years > 1 else ''} and {remaining_months} month{'s' if remaining_months > 1 else ''}"

def calculate_diff_payments(principal, periods, interest):
    i = interest / (12 * 100)
    payments = []
    for m in range(1, periods + 1):
        d = principal / periods + i * (principal - (principal * (m - 1) / periods))
        payments.append(math.ceil(d))
        print(f"Month {m}: payment is {math.ceil(d)}")
    return payments

def validate_args(args):
    required_args = [args.principal, args.payment, args.periods, args.interest]
    if args.interest is None or args.type not in ["annuity", "diff"]:
        return False
    if args.type == "diff" and args.payment is not None:
        return False
    if sum(x is not None for x in required_args) < 3:
        return False
    if any(isinstance(x, (int, float)) and x is not None and x < 0 for x in required_args):
        return False
    return True

def main():
    parser = argparse.ArgumentParser(description="Loan Calculator")
    parser.add_argument("--type", type=str)
    parser.add_argument("--principal", type=float)
    parser.add_argument("--payment", type=float)
    parser.add_argument("--periods", type=int)
    parser.add_argument("--interest", type=float)

    args = parser.parse_args()

    if not validate_args(args):
        print("Incorrect parameters")
        return

    if args.type == "diff":
        payments = calculate_diff_payments(args.principal, args.periods, args.interest)
        overpayment = sum(payments) - int(args.principal)
        print(f"\nOverpayment = {overpayment}")

    elif args.type == "annuity":
        if args.principal and args.payment and not args.periods:
            periods = calculate_number_of_payments(args.principal, args.payment, args.interest)
            readable_period = convert_months_to_years_and_months(periods)
            print(f"It will take {readable_period} to repay this loan!")
            overpayment = args.payment * periods - args.principal
            print(f"Overpayment = {int(overpayment)}")

        elif args.principal and args.periods and not args.payment:
            payment = calculate_annuity_payment(args.principal, args.periods, args.interest)
            print(f"Your annuity payment = {payment}!")
            overpayment = payment * args.periods - args.principal
            print(f"Overpayment = {int(overpayment)}")

        elif args.payment and args.periods and not args.principal:
            principal = calculate_loan_principal(args.payment, args.periods, args.interest)
            print(f"Your loan principal = {principal}!")
            overpayment = args.payment * args.periods - principal
            print(f"Overpayment = {int(overpayment)}")

if __name__ == "__main__":
    main()