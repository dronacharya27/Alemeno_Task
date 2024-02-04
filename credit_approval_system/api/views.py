from rest_framework.viewsets import ModelViewSet
from api.models import Customer, Loan
from api.serializers import CustomerSerializer, LoanSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from dateutil.relativedelta import relativedelta
import random
from api.check_eligiblity import get_credit_score, get_monthly_installment


# Customer View
class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
        if request.method == "POST":
            serializer = CustomerSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = serializer.data
                print(data)
                response_data = {
                    "customer_id": f'{data["customer_id"]}',
                    "name": f'{data["first_name"]}' + f'{data["last_name"]}',
                    "age": data["age"],
                    "monthly_income": data["monthly_salary"],
                    "approved_limit": data["approved_limit"],
                    "phone_number": data["phone_number"],
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Loan View
class LoanViewSet(ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

    def check_eligiblity(self, request):
        if request.method == "POST":
            input_data = {
                "customer": request.data.get("customer_id"),
                "tenure": request.data.get("tenure"),
                "interest_rate": request.data.get("interest_rate"),
                "loan_amount": request.data.get("loan_amount"),
            }
            serializer = LoanSerializer(data=input_data, partial=True)
            if serializer.is_valid():
                customer_id = request.data.get("customer_id")

                loan_amount = request.data.get("loan_amount")
                tenure = request.data.get("tenure")
                interest_rate = request.data.get("interest_rate")
                monthly_installment = 0

                customer = Customer.objects.get(customer_id=customer_id)

                salary = customer.monthly_salary
                corrected_interest_rate = 0
                approval = True
                credit_score = get_credit_score(customer_id)[0]
                current_emi_ammount = get_credit_score(customer_id)[1]
                # Approval of the loan and changes in interest rate
                if credit_score > 50:
                    approval = True
                    corrected_interest_rate = interest_rate

                if 50 > credit_score > 30:
                    approval = True
                    corrected_interest_rate = 12

                if 30 > credit_score > 10:
                    approval = True
                    corrected_interest_rate = 16

                if 10 > credit_score:
                    approval = False
                    corrected_interest_rate = 0

                if current_emi_ammount and current_emi_ammount > (salary / 2):
                    approval = False
                    corrected_interest_rate = 0

                if corrected_interest_rate != 0:
                    monthly_installment = get_monthly_installment(
                        loan_amount=loan_amount,
                        interest_rate=corrected_interest_rate,
                        tenure=tenure,
                    )

                response_data = {
                    "customer_id": customer_id,
                    "approval": approval,
                    "interest_rate": interest_rate,
                    "corrected_interest_rate": corrected_interest_rate,
                    "tenure": tenure,
                    "monthly_installment": round(monthly_installment, 2),
                }

                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create_loan(self, request):
        if request.method == "POST":
            input_data = {
                "customer": request.data.get("customer_id"),
                "tenure": request.data.get("tenure"),
                "interest_rate": request.data.get("interest_rate"),
                "loan_amount": request.data.get("loan_amount"),
            }
            serializer = LoanSerializer(data=input_data, partial=True)
            if serializer.is_valid():
                customer_id = request.data.get("customer_id")

                loan_amount = request.data.get("loan_amount")
                tenure = request.data.get("tenure")
                interest_rate = request.data.get("interest_rate")
                monthly_installment = 0

                customer = Customer.objects.get(customer_id=customer_id)

                salary = customer.monthly_salary
                corrected_interest_rate = 0
                approval = True
                message = "Your loan is Approved Succesfully"
                credit_score = get_credit_score(customer_id)[0]
                current_emi_ammount = get_credit_score(customer_id)[1]
                # Approval of the loan and changes in interest rate

                if credit_score > 50:
                    approval = True
                    corrected_interest_rate = interest_rate

                if 50 > credit_score > 30:
                    approval = True
                    corrected_interest_rate = 12

                if 30 > credit_score > 10:
                    approval = True
                    corrected_interest_rate = 16

                if 10 > credit_score:
                    approval = False
                    corrected_interest_rate = 0
                    message = "Your Credit Score is low"

                if current_emi_ammount and current_emi_ammount > (salary / 2):
                    approval = False
                    corrected_interest_rate = 0
                    message = "Your Current EMI's is larger than your Salary income"

                if corrected_interest_rate != 0:
                    monthly_installment = get_monthly_installment(
                        loan_amount=loan_amount,
                        interest_rate=corrected_interest_rate,
                        tenure=tenure,
                    )

                    start_date = datetime.now().strftime("%Y-%m-%d")
                    end_date = datetime.now() + relativedelta(months=tenure)
                    loan_id = random.randint(1000, 9999)
                    loan = Loan.objects.create(
                        loan_id=loan_id,
                        customer=customer,
                        loan_amount=loan_amount,
                        tenure=tenure,
                        start_date=start_date,
                        end_date=end_date.strftime("%Y-%m-%d"),
                        interest_rate=corrected_interest_rate,
                        monthly_repayment=monthly_installment,
                        emis_paid_on_time=0,
                    )
                    loan.save()

                    response_data = {
                        "loan_id": loan_id,
                        "customer_id": customer_id,
                        "loan_approved": approval,
                        "message": message,
                        "monthly_installment": round(monthly_installment, 2),
                    }
                    return Response(response_data, status=status.HTTP_201_CREATED)

                response_data = {
                    "loan_id": None,
                    "customer_id": customer_id,
                    "loan_approved": approval,
                    "message": message,
                    "monthly_installment": round(monthly_installment, 2),
                }

                return Response(response_data, status=status.HTTP_406_NOT_ACCEPTABLE)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def view_loan(self, request, loan_id, *args, **kwargs):
        try:
            loan = Loan.objects.get(loan_id=loan_id)
        except Loan.DoesNotExist:
            return Response(
                "No loan found with current loan_id", status=status.HTTP_404_NOT_FOUND
            )

        customer = CustomerSerializer(loan.customer)
        response_data = {
            "loan_id": loan_id,
            "customer": customer.data,
            "loan_amount": loan.loan_amount,
            "interest_rate": loan.interest_rate,
            "monthly_installment": loan.monthly_repayment,
            "tenure": loan.tenure,
        }
        return Response(response_data, status=status.HTTP_200_OK)

    def view_customer_loans(self, request, customer_id, *args, **kwargs):
        try:
            Customer.objects.get(customer_id=customer_id)
        except Customer.DoesNotExist:
            return Response(
                "No customer found with current ID", status=status.HTTP_404_NOT_FOUND
            )
        loan = Loan.objects.filter(customer_id=customer_id)
        loan_list = []
        for loan in loan:
            loan_serialized = LoanSerializer(loan)
            loan_list.append(loan_serialized.data)
        if len(loan_list) == 0:
            return Response(
                "No associated loans found with current accont",
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(loan_list, status=status.HTTP_200_OK)
