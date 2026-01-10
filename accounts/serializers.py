from rest_framework import serializers
from .models import Account
from django.contrib.auth import authenticate

class SignUpSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=Account
        fields=['FirstName','LastName','Email','password']
    
    def create(self,validated_data):
        user=Account.objects.create_user(
            Email=validated_data['Email'],
            password=validated_data['password'],
            FirstName=validated_data['FirstName'],
            LastName=validated_data['LastName']
            
        )
        print(f"OTP for {user.Email} : {user.otp} ")
        return user

 
class VerifyOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()
    otp=serializers.CharField(max_length=5)
    
class ResendOtpSerializer(serializers.Serializer):
    email=serializers.EmailField()       



