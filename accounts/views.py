
from allauth.account.signals import password_reset
from django.shortcuts import render, redirect, HttpResponse
from django.template.context_processors import media
from django.utils.text import phone2numeric
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from kavenegar import KavenegarAPI, APIException, HTTPException
from .forms import UserRegistrationForm, VerificationCodeForm, UserLoginForm, CustomUserForm, ForgotPasswordForm,VerificationCodeResetPassForm
from .models import CustomUser
from home.models import imagesTowMadah
from django.contrib.auth.mixins import LoginRequiredMixin
from zeep import Client
import random
from datetime import timedelta , datetime
from django.utils import timezone
import pytz

class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = UserRegistrationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما قبلا وارد شده‌اید', 'primary')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd.get('username')
            phone_number = cd.get('phone_number')
            password = cd.get('password')
            first_name = cd.get('first_name')
            print(first_name)
            last_name = cd.get('last_name')

            # Generate random verification code
            verification_code = random.randint(10000, 100000)

            try:
                api = KavenegarAPI('7137636B3533527375376E4266717465386F712F426153787443696D6E363859714F657A4B3754336434513D')
                params = {
                    'receptor': phone_number,
                    'template': 'register',
                    'token': verification_code,
                    'type': 'sms',
                }
                response = api.verify_lookup(params)
            except (APIException, HTTPException) as e:
                messages.error(request, 'خطایی در ارسال پیامک رخ داده است. لطفاً دوباره تلاش کنید.')
                return render(request, self.template_name, {'form': form})

            # Store verification code and user info in session
            request.session['verification_code'] = verification_code
            request.session['verification_code_sent_time'] = timezone.now().timestamp()
            request.session['username'] = username
            request.session['phone_number'] = phone_number
            request.session['password'] = password
            request.session['first_name'] = first_name
            print(first_name + '1')
            request.session['last_name'] = last_name

            messages.success(request, 'یک کد تایید به شماره شما ارسال شد. لطفاً کد را وارد کنید.', 'success')
            return redirect('accounts:verify_code')
        else:
            messages.error(request, 'فرم ارسال شده معتبر نیست. لطفاً دوباره تلاش کنید.')
            return render(request, self.template_name, {'form': form})

class VerifyCodeView(View):
    template_name = 'accounts/verify_code.html'
    form_class = VerificationCodeForm

    def get(self, request):
        if request.session.get('verification_code'):
            form = self.form_class()
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('home:home')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('code')
            print(entered_code)
            session_code = request.session.get('verification_code')
            sent_time = request.session.get('verification_code_sent_time')
            # تبدیل timestamp به datetime بدون ناحیه زمانی
            sent_time_naive = datetime.fromtimestamp(sent_time)

            # تبدیل datetime به timezone-aware با استفاده از pytz
            sent_time_aware = pytz.utc.localize(sent_time_naive)

            # اطمینان از اینکه timezone.now() نیز timezone-aware است
            now_aware = timezone.now()

            # مقایسه
            if sent_time_aware and now_aware > sent_time_aware + timedelta(minutes=1):
                messages.error(request, 'کد تایید منقضی شده است. لطفاً دوباره درخواست ارسال کد کنید.')
                return redirect('accounts:resend_verification_code')

            if int(entered_code) == int(session_code):
                username = request.session.get('username')
                password = request.session.get('password')
                first_name = request.session.get('first_name')
                last_name = request.session.get('last_name')
                phone_number = request.session.get('phone_number')

                # Create the user
                user = CustomUser.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    phone_number=phone_number
                )

                login(request, user)
                messages.success(request, 'ثبت نام با موفقیت انجام شد.', 'success')
                request.session.flush()
                return redirect('home:home')
            else:
                messages.error(request, 'کد تایید نادرست است.')
        return render(request, self.template_name, {'form': form})

class ResendVerificationCodeView(View):
    def get(self, request):
        phone_number = request.session.get('phone_number')
        if not phone_number:
            messages.error(request, 'شماره موبایل یافت نشد. لطفاً دوباره تلاش کنید.')
            return redirect('accounts:register')

        # تولید و ارسال کد تایید جدید
        verification_code = random.randint(10000, 100000)
        try:
            api = KavenegarAPI('7137636B3533527375376E4266717465386F712F426153787443696D6E363859714F657A4B3754336434513D')
            params = {
                'receptor': phone_number,
                'template': 'resendcode',
                'token': verification_code,
                'type': 'sms',
            }

            response = api.verify_lookup(params)
            request.session['verification_code'] = verification_code
            request.session['verification_code_sent_time'] = timezone.now().timestamp()
            messages.success(request, 'کد جدید به شماره شما ارسال شد.')
            return redirect('accounts:verify_code')
        except (APIException, HTTPException):
            messages.error(request, 'خطایی در ارسال پیامک رخ داده است. لطفاً دوباره تلاش کنید.')
            return redirect('../')


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.success(request, 'شما قبلا وارد شده‌اید', 'primary')
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

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

class ForgotPasswordView(View):
    template_name = 'accounts/reset_pass.html'
    form_class = ForgotPasswordForm
    def get(self , request):
        form = self.form_class()
        return render(request , self.template_name,{'form' : form })
    def post(self,request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data.get('phone_number')
            if not CustomUser.objects.filter(phone_number=phone_number).exists():
                messages.error(request, 'این شماره تلفن یافت نشد','danger')
                return render(request, self.template_name, {'form': self.form_class})
            request.session['verification_code_reset_pass_sent_time'] = timezone.now().timestamp()
            request.session['phone_number_for_reset_pass'] = phone_number
            verification_code = random.randint(10000, 100000)

            try:
                api = KavenegarAPI('7137636B3533527375376E4266717465386F712F426153787443696D6E363859714F657A4B3754336434513D')
                params = {
                    'receptor': phone_number,
                    'template': 'Forgot-password',
                    'token': verification_code,
                    'type': 'sms',
                }
                response = api.verify_lookup(params)
            except (APIException, HTTPException) as e:
                messages.error(request, 'خطایی در ارسال پیامک رخ داده است. لطفاً دوباره تلاش کنید.')

                return render(request, self.template_name, {'form': form})
            request.session['verification_code_for_reset_pass'] = verification_code
            messages.success(request,'کدی به شماره موبایل شما ارسال شد . آن را وارد کنید', 'success')
            return redirect('accounts:verify_code_reset_pass')

class VerifyCodeResetPassView(View):
    template_name = 'accounts/verify_code.html'
    form_class = VerificationCodeResetPassForm

    def get(self, request):
        #if request.session.get('verification_code'):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})
        #else:
            #return redirect('home:home')

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            entered_code = form.cleaned_data.get('code')
            session_code = request.session.get('verification_code_for_reset_pass')
            sent_time = request.session.get('verification_code_sent_time')
            # تبدیل timestamp به datetime بدون ناحیه زمانی
            sent_time_naive = datetime.fromtimestamp(sent_time)

            # تبدیل datetime به timezone-aware با استفاده از pytz
            sent_time_aware = pytz.utc.localize(sent_time_naive)

            # اطمینان از اینکه timezone.now() نیز timezone-aware است
            now_aware = timezone.now()

            # مقایسه
            if sent_time_aware and now_aware > sent_time_aware + timedelta(minutes=1):
                messages.error(request, 'کد تایید منقضی شده است. لطفاً دوباره درخواست ارسال کد کنید.')
                return redirect('../')
            if int(entered_code) == int(session_code):
                phone_number = request.session.get('phone_number')
                user = CustomUser.objects.filter(phone_number=phone_number)
                for user1 in user:
                    user1.set_password(form.cleaned_data.get('password'))
                    user.save()
                # ذخیره تغییرات
                request.session.flush()
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد','success')
                return redirect('accounts:login')

            else:
                messages.error(request, 'کد تایید نادرست است.')
        return render(request, self.template_name, {'form': form})
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
        CallbackURL = 'http://localhost:8000/accounts/verify_payment/'

        client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
        result = client.service.PaymentRequest(merchant, amount, description, '', '', CallbackURL)

        if result.Status == 100:
            return redirect(f'https://www.zarinpal.com/pg/StartPay/{result.Authority}')
        else:
            return HttpResponse(f'Error code: {result.Status}')


class EditProfileView(LoginRequiredMixin, View):
    template_name = 'edit_profile.html'

    def get(self, request):
        form = CustomUserForm(instance=request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = CustomUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            profile = form.save(commit=False)
            profile_picture = profile.profile_picture  # دسترسی به فایل تصویر





            profile.save()  # ذخیره پروفایل با تصویر اصلاح شده
            messages.success(request, 'پروفایل با موفقیت به‌روز شد.', 'success')
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
