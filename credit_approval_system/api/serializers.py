from rest_framework import serializers
from api.models import Customer, Loan
import random

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = [
            "customer_id",
            "first_name",
            "last_name",
            "age",
            "phone_number",
            "monthly_salary",
            "approved_limit",
            "current_debt",
        ]

    def create(self, validated_data):
        monthly_salary = validated_data["monthly_salary"]
        approved_limit = monthly_salary * 36
        remainder = approved_limit % 100000
        if remainder < 50000:
            rounded_approved_limit = approved_limit - remainder
        else:
            rounded_approved_limit = approved_limit + (100000 - remainder)
        customer_id = random.randint(1000,9999)
        customer = Customer(
            customer_id = customer_id,
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
            phone_number=validated_data["phone_number"],
            monthly_salary=validated_data["monthly_salary"],
            age=validated_data["age"],
            approved_limit=rounded_approved_limit,
        )

        customer.save()
        return customer


class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
            "loan_id",
            "customer",
            "loan_amount",
            "tenure",
            "start_date",
            "end_date",
            "interest_rate",
            "monthly_repayment",
            "emis_paid_on_time",
        ]
