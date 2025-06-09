from django.db import models

class OverpaymentCalculation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    tax_year = models.CharField(max_length=10)
    month_op_occurred = models.CharField(max_length=20)
    taxable_pay_ytd = models.DecimalField(max_digits=10, decimal_places=2)
    tax_paid_ytd = models.DecimalField(max_digits=10, decimal_places=2)
    prev_tax_ni_deducted = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Use built-in JSONField → safe for SQLite and Postgres
    paid_data = models.JSONField()
    due_data = models.JSONField()
    difference_data = models.JSONField()

    def __str__(self):
        return f"Overpayment Calculation #{self.id} - {self.tax_year} - {self.month_op_occurred}"
