from django.shortcuts import render
import random
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from .models import Account
from .serializers import SignUpSerializer,VerifyOtpSerializer,ResendOtpSerializer
# Create your views here.

class SignUpView(APIView):
    def post(self,request):
        serializer=SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'User registered successfully .Check terminal for OTP'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

class VerifyOTPView(APIView):
    def post(self,request):
        serializer=VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            Email=serializer.validated_data['Email']
            otp=serializer.validated_data['otp']
            try:
                user=Account.objects.get(Email=Email)
                if user.otp==otp:
                    user.is_active=True
                    user.save()
                    return Response({'message':'OTP verified successfully'})
                return Response({'error','invalid OTP'},status=400)
            except Account.DoesNotExist:
                return Response({'error':'User not found'},status=404)
        return Response(serializer.errors,status=404)
    
class ResendOtpView(APIView):
    def post(self,request):
        serializer=ResendOtpSerializer(data=request.data)
        if serializer.is_valid():
            Email=serializer.validated_data['Email']
            try:
                user=Account.objects.get(Email=Email)
                new_otp=str(random.randint(10000,99999))
                user.otp=new_otp
                user.save()
                print(f"New OTP for {user.Email} is :{user.otp}")
                return Response({"message":"OTP Successfully.checkYour Email"},status=status.HTTP_404_NOT_FOUND)
            except Account.DoesNotExist:
                return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
                
        