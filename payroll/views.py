from rest_framework import viewsets
from .models import PayrollRun
from .serializers import PayrollRunSerializer
from django.http import HttpResponse
from rest_framework.generics import RetrieveAPIView
from .pdf_utils import generate_payslip_pdf

# PayrollRunViewSet → required for router.urls
class PayrollRunViewSet(viewsets.ModelViewSet):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer

# Payslip PDF API
class PayrollRunPayslipPDFAPIView(RetrieveAPIView):
    queryset = PayrollRun.objects.all()
    serializer_class = PayrollRunSerializer

    def get(self, request, *args, **kwargs):
        payroll = self.get_object()
        result = generate_payslip_pdf(payroll)

        if isinstance(result, str):
            return HttpResponse(result, content_type='text/html')
        else:
            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="payslip_{payroll.id}.pdf"'
            return response

