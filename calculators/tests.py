from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import OverpaymentCalculation

class TakeHomeCalculatorTests(APITestCase):
    def test_take_home_calculator(self):
        url = reverse('take-home-calculator')
        data = {
            'gross': 40000,
            'tax_year': '2025',
            'student_loan_plan': 'Plan 2'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tax', response.data)
        self.assertIn('ni', response.data)
        self.assertIn('student_loan', response.data)
        self.assertIn('net', response.data)

class TaxOnlyCalculatorTests(APITestCase):
    def test_tax_only_calculator(self):
        url = reverse('tax-only-calculator')
        data = {'gross': 40000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tax', response.data)

class NIOOnlyCalculatorTests(APITestCase):
    def test_ni_only_calculator(self):
        url = reverse('ni-only-calculator')
        data = {'gross': 40000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ni', response.data)

class StudentLoanOnlyCalculatorTests(APITestCase):
    def test_student_loan_only_calculator(self):
        url = reverse('student-loan-only-calculator')
        data = {'gross': 40000}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('student_loan', response.data)

class OverpaymentCalculationTests(APITestCase):
    def test_overpayment_calculation_post_and_pdf(self):
        post_url = reverse('overpayment-calculator')
        post_data = {
            "tax_year": "2025",
            "month_op_occurred": "December",
            "taxable_pay_ytd": "35000.00",
            "tax_paid_ytd": "6000.00",
            "prev_tax_ni_deducted": "200.00",
            "paid_data": {
                "December": {
                    "tax_code": "1257L",
                    "tax_code_basis": "Cumulative",
                    "ni_category": "A",
                    "pension_percent": 5,
                    "pension_salary_sacrifice": False,
                    "student_loan_plan": "Plan 2",
                    "pensionable_pay": 3000,
                    "gross_pay": 3500,
                    "deductions": {
                        "pension": 150,
                        "paye": 500,
                        "ni": 300,
                        "student_loan": 100,
                        "net_pay": 2450
                    }
                }
            },
            "due_data": {
                "December": {}
            },
            "difference_data": {}
        }

        # Test POST
        post_response = self.client.post(post_url, post_data, format='json')
        self.assertEqual(post_response.status_code, status.HTTP_200_OK)
        self.assertIn('id', post_response.data)

        calculation_id = post_response.data['id']

        # Test PDF fallback GET
        pdf_url = reverse('overpayment-pdf', kwargs={'pk': calculation_id})
        pdf_response = self.client.get(pdf_url)
        self.assertEqual(pdf_response.status_code, status.HTTP_200_OK)

        # If fallback HTML, content type will be text/html
        # If real PDF (when GTK installed), content type will be application/pdf
        self.assertIn(pdf_response['Content-Type'], ['text/html', 'application/pdf'])
