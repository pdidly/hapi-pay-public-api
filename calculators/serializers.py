from rest_framework import serializers
from .models import OverpaymentCalculation

class OverpaymentCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OverpaymentCalculation
        fields = '__all__'