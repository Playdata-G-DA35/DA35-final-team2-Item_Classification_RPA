from typing import Any
from django import forms
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="비밀번호")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="비밀번호 확인")
    first_name = forms.CharField(label="이름")

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'first_name', 'email']
        labels = {
            'username': '아이디',
            'first_name': '이름',
            'email': '이메일'
        }

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise ValidationError("비밀번호가 일치하지 않습니다.")
        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class FindIDForm(forms.Form):
    first_name = forms.CharField(label="이름", max_length=30)
    email = forms.EmailField(label="이메일")
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        email = cleaned_data.get('email')

        if not User.objects.filter(first_name=first_name, email=email).exists():
            raise forms.ValidationError("입력한 정보와 일치하는 사용자가 없습니다.")
        
        return cleaned_data

class FindPasswordForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='아이디',
        help_text='아이디를 입력해주세요.'
    )
    first_name = forms.CharField(
        max_length=30,
        label='이름',
        help_text='이름을 입력해주세요.'
    )
    email = forms.EmailField(
        label='이메일',
        help_text='이메일을 입력해주세요.'
    )

class PasswordResetConfirmForm(forms.Form):
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        label='새 비밀번호',
        help_text='새 비밀번호를 입력해주세요.'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        label='새 비밀번호 확인',
        help_text='새 비밀번호를 한 번 더 입력해주세요.'
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error('confirm_password', "비밀번호가 일치하지 않습니다.")

        if self.user and new_password and self.user.check_password(new_password):
            self.add_error('new_password', "이전 비밀번호와 동일한 비밀번호를 사용할 수 없습니다.")

        return cleaned_data