import datetime


class Loan:
    def __init__(self, interest_rate, balance, outstanding_interest=0):
        self.base_interest_rate = interest_rate
        self.balance = balance
        self.outstanding_interest = outstanding_interest
        self.direct_debit_discount = False

    def generate_interest(self, start, end):
        if start is None:
            return
        delta_days = (end - start).days
        # TODO 366 for leap
        period_interest_rate = self.interest_rate * (delta_days / 365)
        new_interest = period_interest_rate * self.balance
        import ipdb; ipdb.set_trace()
        return new_interest

    def add_interest(self, start, end):
        new_interest = self.generate_interest(start, end)
        self.outstanding_interest += new_interest
        self.outstanding_interest = round(self.outstanding_interest, 2)

    @property
    def interest_rate(self):
        if self.direct_debit_discount:
            return self.base_interest_rate - 0.0025
        else:
            return self.base_interest_rate


class RevisedIBR(Loan):
    def __init__(self, interest_rate, balance, outstanding_interest=0, expected_monthly_payment=0):
        super().__init__(interest_rate, balance, outstanding_interest)
        self.expected_monthly_payment = expected_monthly_payment

    def add_interest(self, start, end):
        """Override"""
        new_interest = self.generate_interest(start, end)
        if new_interest > self.expected_monthly_payment:
            import ipdb; ipdb.set_trace()
            subsidy = (new_interest - self.expected_monthly_payment) / 2
            new_interest -= subsidy
        self.outstanding_interest += new_interest
        self.outstanding_interest = round(self.outstanding_interest, 2)

    @classmethod
    def from_loan(cls, loan, expected_monthly_payment=0):
        return cls(loan.interest_rate, loan.balance,
                   expected_monthly_payment=expected_monthly_payment)




# big = Loan(
#     interest_rate=0.065,
#     balance=66554.27,
#     outstanding_interest=0,
# )
#
# print(big.outstanding_interest)
# start = datetime.date(2018, 9, 6)
# end = datetime.date(2018, 10, 6)
# big.generate_monthly_bill(start, end)
# print(big.outstanding_interest)
# print(big.balance)



