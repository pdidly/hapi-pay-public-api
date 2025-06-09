from django.db import models

class PayrollRun(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    payroll_date = models.DateField()
    original_calculation = models.JSONField()
    corrected_calculation = models.JSONField(blank=True, null=True)
    difference = models.JSONField(blank=True, null=True)
    fps_submitted_original = models.BooleanField(default=False)
    fps_submitted_corrected = models.BooleanField(default=False)
