from celery import shared_task
from api.models import Customer, Loan
import pandas as pd


@shared_task
def ingest_data():
    customer_records = pd.read_excel("./assets/customer_data.xlsx")
    loan_records = pd.read_excel("./assets/loan_data.xlsx")

    for index, row in customer_records.iterrows():
        Customer.objects.create(
            customer_id=row["Customer ID"],
            first_name=row["First Name"],
            last_name=row["Last Name"],
            age=row["Age"],
            phone_number=row["Phone Number"],
            monthly_salary=row["Monthly Salary"],
            approved_limit=row["Approved Limit"],
        )

    for index, row in loan_records.iterrows():
        Loan.objects.create(
            loan_id=row["Loan ID"],
            customer_id=row["Customer ID"],
            loan_amount=row["Loan Amount"],
            tenure=row["Tenure"],
            interest_rate=row["Interest Rate"],
            monthly_repayment=row["Monthly payment"],
            emis_paid_on_time=row["EMIs paid on Time"],
            start_date=row["Date of Approval"],
            end_date=row["End Date"],
        )
