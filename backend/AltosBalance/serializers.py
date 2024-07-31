from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from AltosBalance.models import *

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['user_is_staff'] = user.is_staff

        return token
    
class PaymentTermsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentTerms
        fields = '__all__'