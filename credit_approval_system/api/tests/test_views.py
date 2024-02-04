from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Customer, Loan

class CustomerViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_customer(self):
        url = reverse("register-list")
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "age": 25,
            "phone_number": "1234567890",
            "monthly_salary": 5000,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "JohnDoe")
        self.assertEqual(response.data["age"], 25)
        self.assertEqual(response.data["monthly_income"], 5000)


class LoanViewSetTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_check_eligibility_false(self):
        url = reverse("check-eligiblity")
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        data = {
            "customer_id": customer.customer_id,
            "tenure": 12,
            "interest_rate": 8.0,
            "loan_amount": 10000.0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("customer_id", response.data)
        self.assertIn("approval", response.data)
        self.assertIn("interest_rate", response.data)
        self.assertIn("corrected_interest_rate", response.data)
        self.assertIn("tenure", response.data)
        self.assertIn("monthly_installment", response.data)

    def test_check_eligibility(self):
        url = reverse("check-eligiblity")
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        Loan.objects.create(
            loan_id=2520,
            customer=customer,
            loan_amount=1000000.00,
            tenure=99,
            start_date="2013-10-25",
            end_date="2022-01-25",
            interest_rate=16.19,
            monthly_repayment=33552.00,
            emis_paid_on_time=50,
        )
        Loan.objects.create(
            loan_id=6045,
            customer=customer,
            loan_amount=600000.00,
            tenure=21,
            start_date="2021-12-31",
            end_date="2023-09-30",
            interest_rate=17.86,
            monthly_repayment=33674.00,
            emis_paid_on_time=21,
        )
        Loan.objects.create(
            loan_id=6693,
            customer=customer,
            loan_amount=500000.00,
            tenure=54,
            start_date="2013-05-15",
            end_date="2017-11-15",
            interest_rate=11.56,
            monthly_repayment=14342.00,
            emis_paid_on_time=53,
        )
        Loan.objects.create(
            loan_id=7737,
            customer=customer,
            loan_amount=600000.00,
            tenure=60,
            start_date="2012-04-22",
            end_date="2017-04-22",
            interest_rate=13.25,
            monthly_repayment=18629.00,
            emis_paid_on_time=53,
        )
        Loan.objects.create(
            loan_id=9971,
            customer=customer,
            loan_amount=100000.00,
            tenure=138,
            start_date="2022-11-12",
            end_date="2034-05-12",
            interest_rate=13.23,
            monthly_repayment=2842.00,
            emis_paid_on_time=107,
        )
        Loan.objects.create(
            loan_id=5543,
            customer=customer,
            loan_amount=400000.00,
            tenure=174,
            start_date="2010-05-20",
            end_date="2024-11-20",
            interest_rate=17.94,
            monthly_repayment=23161.00,
            emis_paid_on_time=92,
        )
        Loan.objects.create(
            loan_id=3079,
            customer=customer,
            loan_amount=100000.00,
            tenure=102,
            start_date="2013-06-04",
            end_date="2021-12-04",
            interest_rate=13.22,
            monthly_repayment=2647.00,
            emis_paid_on_time=54,
        )

        data = {
            "customer_id": customer.customer_id,
            "tenure": 12,
            "interest_rate": 8.0,
            "loan_amount": 10000.0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("customer_id", response.data)
        self.assertIn("approval", response.data)
        self.assertIn("interest_rate", response.data)
        self.assertIn("corrected_interest_rate", response.data)
        self.assertIn("tenure", response.data)
        self.assertIn("monthly_installment", response.data)

    def test_check_eligibility_customer_not_found(self):
        url = reverse("check-eligiblity")

        data = {
            "customer_id": 1,
            "tenure": 12,
            "interest_rate": 8.0,
            "loan_amount": 10000.0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_loan_false(self):
        url = reverse("create-loan")
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        data = {
            "customer_id": customer.customer_id,
            "tenure": 12,
            "interest_rate": 8.0,
            "loan_amount": 10000.0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn("loan_id", response.data)
        self.assertIn("customer_id", response.data)
        self.assertIn("loan_approved", response.data)
        self.assertIn("message", response.data)
        self.assertIn("monthly_installment", response.data)

    def test_create_loan(self):
        url = reverse("create-loan")
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        Loan.objects.create(
            loan_id=2520,
            customer=customer,
            loan_amount=1000000.00,
            tenure=99,
            start_date="2013-10-25",
            end_date="2022-01-25",
            interest_rate=16.19,
            monthly_repayment=33552.00,
            emis_paid_on_time=50,
        )
        Loan.objects.create(
            loan_id=6045,
            customer=customer,
            loan_amount=600000.00,
            tenure=21,
            start_date="2021-12-31",
            end_date="2023-09-30",
            interest_rate=17.86,
            monthly_repayment=33674.00,
            emis_paid_on_time=21,
        )
        Loan.objects.create(
            loan_id=6693,
            customer=customer,
            loan_amount=500000.00,
            tenure=54,
            start_date="2013-05-15",
            end_date="2017-11-15",
            interest_rate=11.56,
            monthly_repayment=14342.00,
            emis_paid_on_time=53,
        )
        Loan.objects.create(
            loan_id=7737,
            customer=customer,
            loan_amount=600000.00,
            tenure=60,
            start_date="2012-04-22",
            end_date="2017-04-22",
            interest_rate=13.25,
            monthly_repayment=18629.00,
            emis_paid_on_time=53,
        )
        Loan.objects.create(
            loan_id=9971,
            customer=customer,
            loan_amount=100000.00,
            tenure=138,
            start_date="2022-11-12",
            end_date="2034-05-12",
            interest_rate=13.23,
            monthly_repayment=2842.00,
            emis_paid_on_time=107,
        )
        Loan.objects.create(
            loan_id=5543,
            customer=customer,
            loan_amount=400000.00,
            tenure=174,
            start_date="2010-05-20",
            end_date="2024-11-20",
            interest_rate=17.94,
            monthly_repayment=23161.00,
            emis_paid_on_time=92,
        )
        Loan.objects.create(
            loan_id=3079,
            customer=customer,
            loan_amount=100000.00,
            tenure=102,
            start_date="2013-06-04",
            end_date="2021-12-04",
            interest_rate=13.22,
            monthly_repayment=2647.00,
            emis_paid_on_time=54,
        )
        data = {
            "customer_id": customer.customer_id,
            "tenure": 12,
            "interest_rate": 8.0,
            "loan_amount": 10000.0,
        }

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)
        self.assertIn("loan_id", response.data)
        self.assertIn("customer_id", response.data)
        self.assertIn("loan_approved", response.data)
        self.assertIn("message", response.data)
        self.assertIn("monthly_installment", response.data)

    def test_view_loan(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
        )
        loan = Loan.objects.create(
            loan_id=1,
            customer=customer,
            loan_amount=10000.0,
            tenure=12,
            start_date="2013-10-25",
            end_date="2022-01-25",
            interest_rate=8.0,
            monthly_repayment=900.75,
            emis_paid_on_time=0,
        )
        url = reverse("view-loan", args=[loan.loan_id])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("loan_id", response.data)
        self.assertIn("customer", response.data)
        self.assertIn("loan_amount", response.data)
        self.assertIn("interest_rate", response.data)
        self.assertIn("monthly_installment", response.data)
        self.assertIn("tenure", response.data)

    def test_view_customer_loans(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        Loan.objects.create(
            loan_id=1,
            customer=customer,
            loan_amount=10000.0,
            tenure=12,
            start_date="2013-10-25",
            end_date="2022-01-25",
            interest_rate=8.0,
            monthly_repayment=900.75,
            emis_paid_on_time=0,
        )
        url = reverse("view-loans", args=[customer.customer_id])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(isinstance(response.data, list))

    def test_view_customer_loans_no_customer_found(self):
        url = reverse("view-loans", args=[1])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_view_customer_loans_no_loan_found(self):
        customer = Customer.objects.create(
            first_name="Jane",
            last_name="Smith",
            age=30,
            phone_number="9876543210",
            monthly_salary=6000,
            approved_limit=3500000,
        )
        url = reverse("view-loans", args=[customer.customer_id])

        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
