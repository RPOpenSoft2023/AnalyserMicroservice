from rest_framework import serializers
from .models import monthWiseAnalytics

class MonthWiseAnalyticsSerializer(serializers.ModelSerializer):
    class Meta : 
        model = monthWiseAnalytics
        fields = '__all__'

