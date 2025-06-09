import yaml
from pathlib import Path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from django.http import HttpResponse
from .models import OverpaymentCalculation
from .serializers import OverpaymentCalculationSerializer
from .pdf_utils import generate_overpayment_pdf

# Load HMRC data (helper - can be used for real logic)
def load_hmrc_data(tax_year):
    file_path = Path(__file__).parent / 'hmrc_data' / f'{tax_year}.yaml'
    with open(file_path, 'r') as f:
        return yaml.safe_load(f)

# Take-Home Calculator API
class TakeHomeCalculatorAPIView(APIView):
    def post(self, request):
        gross = float(request.data.get('gross', 0))
        tax_year = request.data.get('tax_year', '2025')  # allow tax_year param

        hmrc_data = load_hmrc_data(tax_year)

        # --- Tax ---
        taxable_income = max(0, gross - hmrc_data['personal_allowance'])
        tax = 0

        # Basic rate
        if taxable_income <= hmrc_data['basic_rate_upper_limit'] - hmrc_data['personal_allowance']:
            tax += taxable_income * (hmrc_data['basic_rate_percent'] / 100)
        else:
            basic_band = hmrc_data['basic_rate_upper_limit'] - hmrc_data['personal_allowance']
            tax += basic_band * (hmrc_data['basic_rate_percent'] / 100)

            remaining = taxable_income - basic_band
            # Higher rate
            if remaining <= hmrc_data['higher_rate_upper_limit'] - hmrc_data['basic_rate_upper_limit']:
                tax += remaining * (hmrc_data['higher_rate_percent'] / 100)
            else:
                higher_band = hmrc_data['higher_rate_upper_limit'] - hmrc_data['basic_rate_upper_limit']
                tax += higher_band * (hmrc_data['higher_rate_percent'] / 100)

                remaining -= higher_band
                # Additional rate
                tax += remaining * (hmrc_data['additional_rate_percent'] / 100)

        # --- National Insurance ---
        ni = 0
        if gross > hmrc_data['ni_primary_threshold']:
            ni_income = gross - hmrc_data['ni_primary_threshold']
            if ni_income <= hmrc_data['ni_upper_earnings_limit'] - hmrc_data['ni_primary_threshold']:
                ni += ni_income * (hmrc_data['ni_class1_primary_percent'] / 100)
            else:
                lower_band = hmrc_data['ni_upper_earnings_limit'] - hmrc_data['ni_primary_threshold']
                ni += lower_band * (hmrc_data['ni_class1_primary_percent'] / 100)
                remaining = ni_income - lower_band
                ni += remaining * (hmrc_data['ni_class1_upper_percent'] / 100)

        # --- Student Loan ---
        sl = 0
        plan = request.data.get('student_loan_plan', 'Plan 2')
        if plan == 'Plan 1':
            threshold = hmrc_data['student_loan_plan_1_threshold']
            percent = hmrc_data['student_loan_plan_1_percent']
        elif plan == 'Plan 2':
            threshold = hmrc_data['student_loan_plan_2_threshold']
            percent = hmrc_data['student_loan_plan_2_percent']
        elif plan == 'Plan 4':
            threshold = hmrc_data['student_loan_plan_4_threshold']
            percent = hmrc_data['student_loan_plan_4_percent']
        elif plan == 'Plan 5':
            threshold = hmrc_data['student_loan_plan_5_threshold']
            percent = hmrc_data['student_loan_plan_5_percent']
        else:
            threshold = 9999999  # No repayment if unknown plan
            percent = 0

        if gross > threshold:
            sl += (gross - threshold) * (percent / 100)

        # --- Net ---
        net = gross - tax - ni - sl

        return Response({
            'gross': gross,
            'tax': round(tax, 2),
            'ni': round(ni, 2),
            'student_loan': round(sl, 2),
            'net': round(net, 2)
        })

# Tax-only calculator
class TaxOnlyCalculatorAPIView(APIView):
    def post(self, request):
        gross = float(request.data.get('gross', 0))
        tax = gross * 0.20  # Example → replace with real logic later
        return Response({
            'gross': gross,
            'tax': tax
        })

# NI-only calculator
class NIOOnlyCalculatorAPIView(APIView):
    def post(self, request):
        gross = float(request.data.get('gross', 0))
        ni = gross * 0.12  # Example → replace with real logic later
        return Response({
            'gross': gross,
            'ni': ni
        })

# Student Loan-only calculator
class StudentLoanOnlyCalculatorAPIView(APIView):
    def post(self, request):
        gross = float(request.data.get('gross', 0))
        sl = gross * 0.09  # Example → replace with real logic later
        return Response({
            'gross': gross,
            'student_loan': sl
        })

# Overpayment Calculation API
class OverpaymentCalculationAPIView(APIView):
    def post(self, request):
        serializer = OverpaymentCalculationSerializer(data=request.data)
        if serializer.is_valid():
            calculation = serializer.save()
            return Response(OverpaymentCalculationSerializer(calculation).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Overpayment PDF download (safe fallback)
class OverpaymentCalculationPDFAPIView(RetrieveAPIView):
    queryset = OverpaymentCalculation.objects.all()
    serializer_class = OverpaymentCalculationSerializer

    def get(self, request, *args, **kwargs):
        calculation = self.get_object()
        result = generate_overpayment_pdf(calculation)

        if isinstance(result, str):
            # Fallback HTML
            return HttpResponse(result, content_type='text/html')
        else:
            # Proper PDF
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="overpayment_{calculation.id}.pdf"'
            return response
