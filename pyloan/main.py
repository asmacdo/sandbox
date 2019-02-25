from models.loan import Loan, RevisedIBR
from importers.payment_csv import read_data

data = read_data("example_data/direct_big_unsub_payments.csv")
data = data.reindex(index=data.index[::-1])

for idx in data.index[-2::]:
    if idx == 1:
        loan = Loan(interest_rate=0.065, balance=data['Balance'][idx + 1])
    if idx == 0:
        loan = RevisedIBR.from_loan(loan, expected_monthly_payment=262.95)
    end = data["Effective Date"][idx]
    try:
        start = data["Effective Date"][idx + 1]
    except Exception as e:
        start = None
    # if idx == 0:
    #     loan.interest_rate -= 0.0025
    #     import ipdb; ipdb.set_trace()
    loan.add_interest(start, end)
    actual_interest = data['Interest'][idx]
    print(f"Date: {end} | Calc interest: {loan.outstanding_interest} | Actual: {actual_interest}")
    loan.outstanding_interest -= actual_interest
    print(end)
