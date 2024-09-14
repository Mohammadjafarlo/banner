# urls.py
from django.urls import path, include
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('verify/', VerifyCodeView.as_view(), name='verify_code'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('verify_payment/', VerifyPaymentView.as_view(), name='verify_payment'),
    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
    path('Reset_password/', ForgotPasswordView.as_view(), name='Reset_password'),
    path('verify_reset_pass/', VerifyCodeResetPassView.as_view(), name='verify_code_reset_pass'),
    path('resend_verification_code/', ResendVerificationCodeView.as_view(), name='resend_verification_code'),

]
