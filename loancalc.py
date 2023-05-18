import tkinter as tk
from dataclasses import dataclass


@dataclass
class LoanDesc:
    amount: float
    rate: float
    term: int


@dataclass
class Repayment:
    principal: float
    interest: float
    balance: float


@dataclass
class LoanRepayment:
    monthly_payment: float
    monthly_schedule: tuple[Repayment, ...]
    annual_schedule:  tuple[Repayment, ...]
    total: Repayment


def calculate_mortgage(loan: LoanDesc) -> LoanRepayment:
    monthly_rate = loan.rate / 100 / 12
    total_payments = loan.term * 12
    monthly_payment = (loan.amount * monthly_rate) / (1 - (1 + monthly_rate) ** -total_payments)
    monthly_schedule = []
    annual_schedule = []
    balance = loan.amount

    for month in range(total_payments):
        interest = balance * monthly_rate
        principal = monthly_payment - interest
        balance -= principal
        monthly_schedule.append(Repayment(principal, interest, balance))

        if month % 12 == 11:
            annual_schedule.append(
                Repayment(
                    sum(monthly.principal for monthly in monthly_schedule[-12:]),
                    sum(monthly.interest for monthly in monthly_schedule[-12:]),
                    balance
                )
            )

    if (total_payments-1) % 12 != 11:
        annual_schedule.append(
            Repayment(
                sum(monthly.principal for monthly in monthly_schedule[-total_payments%12:]),
                sum(monthly.interest for monthly in monthly_schedule[-total_payments%12:]),
                balance
            )
        )

    return LoanRepayment(
        monthly_payment=monthly_payment,
        monthly_schedule=tuple(monthly_schedule),
        annual_schedule=tuple(annual_schedule),
        total=Repayment(loan.amount, monthly_payment*total_payments-loan.amount, 0),
    )


# ... the rest of the code ...

# Create Tkinter window
window = tk.Tk()
window.title("Mortgage Calculator")

# Create Tkinter widgets for input fields and labels
loan_amount_label = tk.Label(window, text="Loan Amount ($):")
loan_amount_var = tk.DoubleVar(value=100000.0)
loan_amount_entry = tk.Entry(window, textvariable=loan_amount_var)

loan_rate_label = tk.Label(window, text="Annual Loan Rate (%):")
loan_rate_var = tk.DoubleVar(value=5.0)
loan_rate_entry = tk.Entry(window, textvariable=loan_rate_var)


loan_term_label = tk.Label(window, text="Loan Term (in years):")
loan_term_var = tk.IntVar(value=30)
loan_term_entry = tk.Entry(window, textvariable=loan_term_var)

# Function to calculate mortgage and display results
def calculate_and_display():
    loan_amount = loan_amount_var.get()
    loan_rate = loan_rate_var.get()
    loan_term = loan_term_var.get()

    mortgage_data = LoanDesc(amount=loan_amount, rate=loan_rate, term=loan_term)
    repayment = calculate_mortgage(mortgage_data)
    print(repayment.monthly_payment)

    result_label = tk.Label(window, text=f"The monthly mortgage payment is: ${repayment.monthly_payment:,.2f}")
    result_label.grid(row=4, columnspan=2)

# Tkinter button to trigger calculation and display of results
calculate_button = tk.Button(window, text="Calculate", command=calculate_and_display)

# Use grid layout manager to organize widgets

loan_amount_label.grid(row=0, column=0)
loan_amount_entry.grid(row=0, column=1)
loan_rate_label.grid(row=1, column=0)
loan_rate_entry.grid(row=1, column=1)
loan_term_label.grid(row=2, column=0)
loan_term_entry.grid(row=2, column=1)
calculate_button.grid(row=3, columnspan=2)

window.mainloop()


def get_input() -> LoanDesc:
    default = LoanDesc(amount=100000, rate=5, term=30)
    loan_amount = float(input(f'Enter the loan amount (${default.amount:,.2f}): ') or f'{default.amount}')
    loan_rate = float(input(f'Enter the annual loan rate (%{default.rate}): ') or f'{default.rate}')
    loan_term = int(input(f'Enter the loan term (in years, {default.term}): ') or f'{default.term}')
    return LoanDesc(amount=loan_amount, rate=loan_rate, term=loan_term)


def display_output(repayment: LoanRepayment):
    print(f"The monthly mortgage payment is: ${repayment.monthly_payment:,.2f}")

    for year, annualy in enumerate(repayment.annual_schedule, start=1):
        print(f"Year {year}: principal=${annualy.principal:,.2f}, interest=${annualy.interest:,.2f}, balance=${annualy.balance:,.2f}")

    print()

    for month, monthly in enumerate(repayment.monthly_schedule, start=1):
        print(f"Month {month}: principal=${monthly.principal:,.2f}, interest=${monthly.interest:,.2f}, balance=${monthly.balance:,.2f}")


def main():
    mortgage_data = get_input()
    repayment = calculate_mortgage(mortgage_data)
    display_output(repayment)


#main()

