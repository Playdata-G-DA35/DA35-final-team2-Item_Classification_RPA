from django import forms
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
