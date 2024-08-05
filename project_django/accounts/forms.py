from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    nickname = forms.CharField(max_length=50, required=True, label='닉네임:')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # 'nickname' 필드를 포함하지 않음

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디:'
        self.fields['email'].label = 'Email:'
        self.fields['password1'].label = '비밀번호:'
        self.fields['password2'].label = '비밀번호 확인:'
    
    def clean_nickname(self):
        nickname = self.cleaned_data.get('nickname')
        if Profile.objects.filter(nickname=nickname).exists():
            raise forms.ValidationError('닉네임이 이미 존재합니다.')
        return nickname

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = '아이디:'
        self.fields['password'].label = '비밀번호:'
