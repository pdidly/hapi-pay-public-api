from django.urls import path, include

urlpatterns = [
    path('api/calculators/', include('calculators.urls')),
    path('api/payroll/', include('payroll.urls')),
]
