# Generated by Django 5.0.1 on 2024-02-04 21:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Customer",
            fields=[
                ("customer_id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=50)),
                ("last_name", models.CharField(max_length=50)),
                ("age", models.IntegerField()),
                ("phone_number", models.BigIntegerField()),
                ("monthly_salary", models.BigIntegerField()),
                ("approved_limit", models.BigIntegerField(blank=True, null=True)),
                ("current_debt", models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Loan",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("loan_id", models.IntegerField()),
                ("loan_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("tenure", models.IntegerField()),
                ("start_date", models.DateField()),
                ("end_date", models.DateField()),
                ("interest_rate", models.FloatField()),
                (
                    "monthly_repayment",
                    models.DecimalField(decimal_places=2, max_digits=10),
                ),
                ("emis_paid_on_time", models.IntegerField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.customer"
                    ),
                ),
            ],
        ),
    ]
