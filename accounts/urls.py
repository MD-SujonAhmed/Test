from django.urls import path
from.views import(
    SignUpView,
    VerifyOTPView,
    ResendOtpView
)
urlpatterns = [
    path('signup/',SignUpView.as_view(),name='SingUp'),
    path('verify-otp/',VerifyOTPView.as_view(),name='Verify-Otp'),
    path('resend-otp/',ResendOtpView.as_view(),name='Resend-Otp'),
    
]
