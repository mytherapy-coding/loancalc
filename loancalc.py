import tkinter as tk
from loan import *


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

    result_label = tk.Label(window, text=f"The monthly mortgage payment is ${repayment.monthly_payment:,.2f}")
    result_label.grid(row=4, columnspan=2)

    resultint_label = tk.Label(window, text=f"The total interest is ${repayment.total.interest:,.2f}")
    resultint_label.grid(row=5, columnspan=2)

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


