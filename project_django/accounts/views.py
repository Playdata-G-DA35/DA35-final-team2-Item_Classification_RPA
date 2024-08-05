from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, CustomAuthenticationForm
from .models import Profile
from django.db import IntegrityError

def signup_view(request):
    """
    회원가입 뷰 함수
    - GET 요청 시 회원가입 폼을 렌더링
    - POST 요청 시 폼 데이터를 처리하여 사용자를 생성하고 홈으로 리다이렉트
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                Profile.objects.create(user=user, nickname=form.cleaned_data.get('nickname'))
                messages.success(request, '회원가입이 완료되었습니다.')
                return redirect('home')  # 홈으로 리다이렉트
            except IntegrityError:
                messages.error(request, '닉네임이 이미 존재합니다.')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    """
    로그인 뷰 함수
    - GET 요청 시 로그인 폼을 렌더링
    - POST 요청 시 폼 데이터를 처리하여 사용자를 인증하고 홈으로 리다이렉트
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # 로그인 후 프로필 확인 및 생성
                if not hasattr(user, 'profile'):
                    Profile.objects.create(user=user, nickname=user.username)  # 기본 닉네임 설정
                return redirect('home')
            else:
                messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
        else:
            messages.error(request, '아이디 또는 비밀번호가 올바르지 않습니다.')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    로그아웃 뷰 함수
    - 사용자를 로그아웃 시키고 홈으로 리다이렉트
    """
    logout(request)
    return redirect('home')

@login_required
def profile_view(request):
    """
    프로필 뷰 함수
    - 로그인한 사용자의 프로필 페이지를 렌더링
    """
    profile = Profile.objects.get(user=request.user)
    return render(request, 'accounts/profile.html', {'profile': profile})