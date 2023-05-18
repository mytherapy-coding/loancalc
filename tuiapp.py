from loan import *


def get_input() -> LoanDesc:
    default = LoanDesc(amount=100000, rate=5, term=30)
    loan_amount = float(input(
        f'Enter the loan amount (${default.amount:,.2f}): ') or f'{default.amount}')
    loan_rate = float(
        input(f'Enter the annual loan rate (%{default.rate}): ') or f'{default.rate}')
    loan_term = int(
        input(f'Enter the loan term (in years, {default.term}): ') or f'{default.term}')
    return LoanDesc(amount=loan_amount, rate=loan_rate, term=loan_term)


def display_output(repayment: LoanRepayment):
    print(
        f"The monthly mortgage payment is: ${repayment.monthly_payment:,.2f}")

    for year, annualy in enumerate(repayment.annual_schedule, start=1):
        print(f"Year {year}: principal=${annualy.principal:,.2f}, interest=${annualy.interest:,.2f}, balance=${annualy.balance:,.2f}")

    print()

    for month, monthly in enumerate(repayment.monthly_schedule, start=1):
        print(f"Month {month}: principal=${monthly.principal:,.2f}, interest=${monthly.interest:,.2f}, balance=${monthly.balance:,.2f}")


def main():
    mortgage_data = get_input()
    repayment = calculate_mortgage(mortgage_data)
    display_output(repayment)


main()
