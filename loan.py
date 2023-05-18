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

