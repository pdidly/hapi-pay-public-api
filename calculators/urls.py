from django.urls import path
from .views import (
    TakeHomeCalculatorAPIView,
    TaxOnlyCalculatorAPIView,
    NIOOnlyCalculatorAPIView,
    StudentLoanOnlyCalculatorAPIView,
    OverpaymentCalculationAPIView,
    OverpaymentCalculationPDFAPIView
)

urlpatterns = [
    path('take-home/', TakeHomeCalculatorAPIView.as_view(), name='take-home-calculator'),
    path('tax-only/', TaxOnlyCalculatorAPIView.as_view(), name='tax-only-calculator'),
    path('ni-only/', NIOOnlyCalculatorAPIView.as_view(), name='ni-only-calculator'),
    path('student-loan-only/', StudentLoanOnlyCalculatorAPIView.as_view(), name='student-loan-only-calculator'),
    path('overpayment/', OverpaymentCalculationAPIView.as_view(), name='overpayment-calculator'),
    path('overpayment/<int:pk>/pdf/', OverpaymentCalculationPDFAPIView.as_view(), name='overpayment-pdf'),
]
