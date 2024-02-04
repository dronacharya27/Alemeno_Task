from api.models import Loan, Customer
from datetime import datetime
from django.db.models import Sum, F


def get_credit_score(id):
    loan_detail = Loan.objects.filter(customer_id=id)
    current_year = datetime.now().year

    # Priority weights for each factors
    past_loan_paid_weight = 0.35
    no_of_loans_weight = 0.30
    current_year_loan_weight = 0.15
    current_loan_amount_weight = 0.10
    approved_limit_weight = 0.20

    # Past Loans paid on time 10 point for one loan
    past_loan_paid_on_time = loan_detail.filter(
        end_date__year__lt=current_year, tenure__exact=F("emis_paid_on_time")
    ).count()

    # Number of loans taken in past 10 points for one loan
    no_of_loans = loan_detail.count()

    # Loan Activity in current year 10 points for one loan
    current_year_loan = loan_detail.filter(end_date__gt=datetime.now()).count()

    # Loan Approved Volume 1 points for 100000 of amount
    customer_detail = Customer.objects.get(customer_id=id)
    approved_limit = int(customer_detail.approved_limit)

    # Loan Ammount
    ongoing_loan_amount = loan_detail.exclude(end_date__year__lt=current_year)
    current_loan_amount = 0

    for loan_amount in ongoing_loan_amount:
        current_loan_amount += int(loan_amount.loan_amount)

    if current_loan_amount > approved_limit:
        credit_score = 0

    else:
        credit_score = (
            past_loan_paid_on_time * 10 * past_loan_paid_weight
            + no_of_loans * 10 * no_of_loans_weight
            + current_year_loan * 10 * current_year_loan_weight
            + current_loan_amount / 100000 * current_loan_amount_weight
            + approved_limit / 100000 * approved_limit_weight
        )
        pass

    sum_of_all_emis = loan_detail.exclude(end_date__year__lt=current_year).aggregate(emi_amount=Sum("monthly_repayment"))

    return round(credit_score, 2), sum_of_all_emis["emi_amount"]


def get_monthly_installment(loan_amount, interest_rate, tenure):
    p = loan_amount
    r = interest_rate / 12 / 100
    n = tenure

    monthly_installment = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)

    return monthly_installment
