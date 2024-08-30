import random
import string
import baner.settings as settings

from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views import View
from django.contrib import messages
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from zeep import Client
from .models import CustomUser
from home.models import imagesTowMadah
from kavenegar import KavenegarAPI, APIException, HTTPException
from django.contrib.auth.decorators import login_required

def clean_phone_number(phone_number):
    """ Clean and format the phone number. """
    if phone_number.startswith('0'):
        return phone_number[1:]
    elif phone_number.startswith('+98'):
        return phone_number[3:]
    return phone_number

class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما قبلا وارد شده‌اید', 'primary')
            return redirect('home:home')
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            phone_number = f'+98{clean_phone_number(cd.get('phone_number'))}'
            password = cd.get('password')
            first_name = cd.get('first_name')
            last_name = cd.get('last_name')

            # Generate random verification code
            verification_code = random.randint(9999, 100000)

            try:
                api = KavenegarAPI('YOUR_API_KEY')  # Replace with your actual API key
                params = {
                    'receptor': phone_number,
                    'template': 'register',
                    'token': verification_code,
                    'type': 'sms',
                }
                response = api.verify_lookup(params)
                print(response)
            except APIException as e:
                print(e)
            except HTTPException as e:
                print(e)

            # Store verification code and user info in session
            request.session['verification_code'] = verification_code
            request.session['username'] = username
            request.session['phone_number'] = phone_number
            request.session['password'] = password
            request.session['first_name'] = first_name
            request.session['last_name'] = last_name

            messages.success(request, 'یک کد تایید به شماره شما ارسال شد. لطفاً کد را وارد کنید.', 'success')
            return redirect('accounts:verify_code')
        else:
            return render(request, self.template_name, {'form': form})

class VerifyCodeView(View):
    template_name = 'accounts/verify_code.html'
    form_class = VerificationCodeForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('code')
            session_code = request.session.get('verification_code')

            if str(entered_code) == str(session_code):
                username = request.session.get('username')
                password = request.session.get('password')
                first_name = request.session.get('first_name')
                last_name = request.session.get('last_name')
                phone_number = request.session.get('phone_number')

                if not first_name or not last_name:
                    messages.error(request, 'خطایی در ثبت‌نام رخ داده است. لطفاً دوباره تلاش کنید.')
                    return redirect('accounts:register')

                # Create user with CustomUser model
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number,
                )

                messages.success(request, 'ثبت نام شما با موفقیت انجام شد. حالا وارد شوید', 'success')
                return redirect('accounts:login')
            else:
                messages.error(request, 'کد تایید نادرست است. لطفاً دوباره تلاش کنید.', 'error')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})

class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما قبلا وارد شده‌اید', 'primary')
            return redirect('home:home')
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'شما وارد شدید', 'success')
                return redirect('home:home')
            messages.error(request, 'نام کاربری و یا رمز عبور نادرست است', 'warning')
        return render(request, self.template_name, {'form': form})

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما با موفقیت خارج شدید', 'warning')
        return redirect('home:home')

class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request):
        user = request.user
        products = imagesTowMadah.objects.filter(created=user)
        return render(request, self.template_name, {'user': user, 'objects': products})

class PaymentView(View):
    def get(self, request):
        shenaseh_generated = request.session.get('shenaseh_generated')
        banner_price = request.session.get('banner_price')

        if not shenaseh_generated or not banner_price:
            return HttpResponse("بنر معتبر پیدا نشد.")

        merchant = 'YOUR_MERCHANT_ID'
        amount = int(banner_price)
        description = "خرید بنر"

        mobile = ''  # Optional
        CallbackURL = 'http://localhost:8000/accounts/verify_payment/'

        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(merchant, amount, description, '', mobile, CallbackURL)

        if result.Status == 100:
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{result.Authority}')
        else:
            return HttpResponse(f'Error code: {result.Status}')

class EditProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/edit_profile.html'

    def get(self, request):
        form = CustomUserForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
        return render(request, self.template_name, {'form': form})

class VerifyPaymentView(View):
    def get(self, request):
        merchant = 'YOUR_MERCHANT_ID'
        authority = request.GET.get('Authority')
        amount = request.session.get('banner_price')

        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentVerification(merchant, authority, amount)

        if result.Status == 100:
            messages.success(request, 'پرداخت شما با موفقیت انجام شد.', 'success')
            # Handle banner purchase (e.g., record in database)
            return redirect('home:home')
        else:
            messages.error(request, 'پرداخت ناموفق بود. لطفاً دوباره تلاش کنید.', 'error')
            return redirect('home:banner_list')
