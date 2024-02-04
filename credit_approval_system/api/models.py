from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    phone_number = models.IntegerField()
    monthly_salary = models.IntegerField()
    approved_limit = models.IntegerField(null=True, blank=True)
    current_debt = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.first_name
    

class Loan(models.Model):
    loan_id = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    interest_rate = models.FloatField()
    monthly_repayment = models.DecimalField(max_digits=10, decimal_places=2)
    emis_paid_on_time = models.IntegerField()

    def __str__(self) -> str:
       return self.loan_id
