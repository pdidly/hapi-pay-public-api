from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import PayrollRun
from django.utils.timezone import now

class PayrollRunTests(APITestCase):
    def test_create_and_retrieve_payroll_run(self):
        # POST create
        url = reverse('payrollrun-list')  # from DefaultRouter
        post_data = {
            'payroll_date': now().date().isoformat(),
            'original_calculation': {
                'gross': 40000,
                'tax': 8000,
                'ni': 4800,
                'student_loan': 3600,
                'net': 23600
            },
            'corrected_calculation': {},
            'difference': {},
            'fps_submitted_original': False,
            'fps_submitted_corrected': False
        }

        post_response = self.client.post(url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        self.assertIn('id', post_response.data)

        run_id = post_response.data['id']

        # GET retrieve
        get_url = reverse('payrollrun-detail', kwargs={'pk': run_id})
        get_response = self.client.get(get_url)
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data['id'], run_id)
        self.assertEqual(get_response.data['original_calculation']['gross'], 40000)

    def test_list_payroll_runs(self):
        # Create a run first
        PayrollRun.objects.create(
            payroll_date=now().date(),
            original_calculation={'gross': 30000, 'tax': 5000, 'ni': 3600, 'student_loan': 2700, 'net': 18700},
            corrected_calculation={},
            difference={},
            fps_submitted_original=False,
            fps_submitted_corrected=False
        )

        # GET list
        url = reverse('payrollrun-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)
    def test_payslip_pdf_endpoint(self):
        # First create a PayrollRun
        payroll_run = PayrollRun.objects.create(
            payroll_date=now().date(),
            original_calculation={'gross': 30000, 'tax': 5000, 'ni': 3600, 'student_loan': 2700, 'net': 18700},
            corrected_calculation={},
            difference={},
            fps_submitted_original=False,
            fps_submitted_corrected=False
        )

        # Now test the PDF endpoint
        pdf_url = reverse('payrollrun-payslip-pdf', kwargs={'pk': payroll_run.id})
        pdf_response = self.client.get(pdf_url)
        self.assertEqual(pdf_response.status_code, status.HTTP_200_OK)
        self.assertIn(pdf_response['Content-Type'], ['text/html', 'application/pdf'])
