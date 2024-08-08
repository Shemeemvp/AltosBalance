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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class DistributorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Distributor
        fields = '__all__'

class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'

class ModulesListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modules_List
        fields = '__all__'

class CNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CNotification
        fields = '__all__'

class ANotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ANotification
        fields = '__all__'

class DNotificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNotification
        fields = '__all__'