from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PayrollRunViewSet
from .views import PayrollRunPayslipPDFAPIView

router = DefaultRouter()
router.register('runs', PayrollRunViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('runs/<int:pk>/payslip/pdf/', PayrollRunPayslipPDFAPIView.as_view(), name='payrollrun-payslip-pdf'),

]
