from django.test import TestCase
from api.models import Customer, Loan
from api.serializers import CustomerSerializer, LoanSerializer
from datetime import date


class CustomerSerializerTestCase(TestCase):
    def test_create_customer(self):
        serializer_data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 25,
            "phone_number": 1234567890,
            "monthly_salary": 5000,
        }

        serializer = CustomerSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())

        # Call the create method to save the customer
        created_customer = serializer.create(serializer.validated_data)

        # Retrieve the customer from the database
        retrieved_customer = Customer.objects.get(
            customer_id=created_customer.customer_id
        )

        # Check if the data is saved correctly
        self.assertEqual(retrieved_customer.first_name, "John")
        self.assertEqual(retrieved_customer.last_name, "Doe")
        self.assertEqual(retrieved_customer.age, 25)
        self.assertEqual(retrieved_customer.phone_number, 1234567890)
        self.assertEqual(retrieved_customer.monthly_salary, 5000)


class LoanSerializerTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number=9876543210,
            monthly_salary=6000,
        )

    def test_create_loan(self):
        serializer_data = {
            "loan_id": 1,
            "customer": self.customer.customer_id,
            "loan_amount": 10000.50,
            "tenure": 12,
            "start_date": date(2023, 1, 1),
            "end_date": date(2023, 12, 31),
            "interest_rate": 5.0,
            "monthly_repayment": 900.75,
            "emis_paid_on_time": 10,
        }

        serializer = LoanSerializer(data=serializer_data)
        self.assertTrue(serializer.is_valid())

        # Call the create method to save the loan
        created_loan = serializer.create(serializer.validated_data)

        # Retrieve the loan from the database
        retrieved_loan = Loan.objects.get(loan_id=created_loan.loan_id)

        # Check if the data is saved correctly
        self.assertEqual(retrieved_loan.loan_id, 1)
        self.assertEqual(retrieved_loan.customer, self.customer)
        self.assertAlmostEqual(retrieved_loan.loan_amount, 10000.50)
        self.assertEqual(retrieved_loan.tenure, 12)
        self.assertEqual(retrieved_loan.start_date, date(2023, 1, 1))
        self.assertEqual(retrieved_loan.end_date, date(2023, 12, 31))
        self.assertAlmostEqual(retrieved_loan.interest_rate, 5.0)
        self.assertAlmostEqual(retrieved_loan.monthly_repayment, 900.75)
        self.assertEqual(retrieved_loan.emis_paid_on_time, 10)
