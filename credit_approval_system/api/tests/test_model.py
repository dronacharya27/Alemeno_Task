from django.test import TestCase
from ..models import Customer, Loan
from datetime import date


class CustomerModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="John",
            last_name="Doe",
            age=30,
            phone_number=1234567890,
            monthly_salary=5000,
        )

    def test_customer_creation(self):
        self.assertEqual(self.customer.first_name, "John")
        self.assertEqual(self.customer.last_name, "Doe")
        self.assertEqual(self.customer.age, 30)
        self.assertEqual(self.customer.phone_number, 1234567890)
        self.assertEqual(self.customer.monthly_salary, 5000)
        self.assertIsNone(self.customer.approved_limit)
        self.assertIsNone(self.customer.current_debt)


class LoanModelTestCase(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=25,
            phone_number=9876543210,
            monthly_salary=6000,
        )
        self.loan = Loan.objects.create(
            loan_id=1,
            customer=self.customer,
            loan_amount=10000.50,
            tenure=12,
            start_date=date(2023, 1, 1),
            end_date=date(2023, 12, 31),
            interest_rate=5.0,
            monthly_repayment=900.75,
            emis_paid_on_time=10,
        )

    def test_loan_creation(self):
        self.assertEqual(self.loan.loan_id, 1)
        self.assertEqual(self.loan.customer, self.customer)
        self.assertAlmostEqual(self.loan.loan_amount, 10000.50)
        self.assertEqual(self.loan.tenure, 12)
        self.assertEqual(self.loan.start_date, date(2023, 1, 1))
        self.assertEqual(self.loan.end_date, date(2023, 12, 31))
        self.assertAlmostEqual(self.loan.interest_rate, 5.0)
        self.assertAlmostEqual(self.loan.monthly_repayment, 900.75)
        self.assertEqual(self.loan.emis_paid_on_time, 10)
