
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


from loan import *

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):

    return """
        <html>
        <head>
            <title>Mortgage Calculator</title>
        </head>
        <body>
            <h1>Mortgage Calculator</h1>
            <form action="/calculate-mortgage" method="POST">
                <label for="amount">Loan Amount:</label>
                <input type="number" id="amount" name="amount" step="0.01"><br><br>

                <label for="rate">Interest Rate:</label>
                <input type="number" id="rate" name="rate" step="0.01"><br><br>

                <label for="term">Loan Term (in years):</label>
                <input type="number" id="term" name="term"><br><br>

                <button type="submit">Calculate</button>
            </form>

            <div id="result">
                {% if monthly_payment %}
                    <h2>Monthly Payment:</h2>
                    <p>{{ monthly_payment }}</p>
                {% endif %}
            </div>
        </body>
        </html>
    """


@app.post("/calculate-mortgage")
async def post_calculate_mortgage(request: Request, amount: float=Form(...), rate: float=Form(...), term: int=Form(...)):
    loan = LoanDesc(amount=amount, rate=rate, term=term)
    print(loan)
    res = calculate_mortgage(loan)
    
    return {
        "monthly_payment": res.monthly_payment
    }


