from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class UserRegistrationForm(forms.Form):
    name = forms.CharField(
        label='نام',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
        error_messages={'required': 'نام اجباری است'}
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        max_length=20,
        widget=forms.TextInput(attrs={'class': 'form-control col-6'}),
        error_messages={'required': 'نام خانوادگی اجباری است'}
    )
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': 'نام کاربری اجباری است'}
    )
    phone_number = forms.CharField(
        label='شماره تلفن',
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control', 'oninput':"handleInputChange(event)",'id':"number"}),
        error_messages={'required': 'شماره تلفن اجباری است', 'invalid': 'شماره تلفن نامعتبر است'}
    )
    password = forms.CharField(
        label='ایجاد رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': '.....', 'class': 'form-control'}),
        error_messages={'required': 'رمز عبور اجباری است'}
    )
    password1 = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': '.....', 'class': 'form-control'}),
        error_messages={'required': 'تکرار رمز عبور اجباری است'}
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('این نام کاربری تکراری است')
        return username

    def clean_phone_number(self):
        phone_number = f'+98{self.cleaned_data.get('phone_number')}'
        if CustomUser.objects.filter(phone_number=phone_number).exists():
            raise ValidationError('این شماره تلفن تکراری است')
        return phone_number

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('password1')

        if p1 and p2:
            if p1 != p2:
                self.add_error('password1', 'رمز ها باید یکی باشند')
            if len(p1) < 6:
                self.add_error('password', 'رمز عبور باید حداقل ۶ کاراکتر باشد')
        return cleaned_data

    def save(self):
        user = CustomUser(
            first_name=self.cleaned_data['name'],
            last_name=self.cleaned_data['last_name'],
            username=self.cleaned_data['username'],
            phone_number=self.cleaned_data['phone_number'],
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user

class VerificationCodeForm(forms.Form):
    code = forms.IntegerField(
        label='کد تایید',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'کد پیامک شده'}),
        error_messages={'required': 'کد تایید الزامی است'}
    )

class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری و یا شماره تلفن',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages={'required': '<strong>نام کاربری</strong> اجباری است'}
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={'placeholder': '.....', 'class': 'form-control'}),
        error_messages={'required': '<strong>رمز عبور</strong> اجباری است'}
    )


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

