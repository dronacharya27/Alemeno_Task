from django.contrib import admin

from api.models import Customer, Loan


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "customer_id",
        "first_name",
        "phone_number",
        "monthly_salary",
        "approved_limit",
        "current_debt",
    ]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "loan_id",
        "customer",
        "loan_amount",
        "tenure",
        "interest_rate",
        "monthly_repayment",
        "emis_paid_on_time",
    ]
