# views.py
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductX, ProductFile
from .forms import RegisterForm, FindIDForm, FindPasswordForm, PasswordResetConfirmForm

def home(request):
    products = Product.objects.all()
    reversed_files = ProductX.objects.all()
    return render(request, 'HOM.html', {'products': products, 'reversed_files': reversed_files})

def file_detail(request, file_id):
    file = get_object_or_404(ProductFile, product_file=file_id)
    return render(request, 'PRD.html', {'file': file})

def product_x_detail(request, product_x_id):
    file = get_object_or_404(ProductX, product_x_id=product_x_id)
    return render(request, 'PRD.html', {'file': file})

def delete_product(request, product_id):
    product = get_object_or_404(Product, product_id=product_id)
    product.delete()
    return redirect('home')

def sell_product(request):
    # Implement this view
    return render(request, 'ADD.html')

def chat(request):
    # Implement this view
    return render(request, 'CHT.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # 로그인 성공 후 리다이렉션
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        form = AuthenticationForm()
    return render(request, 'LOG.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home') # 로그아웃 후 홈 페이지로 리다이렉션

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'{username}님, 회원가입이 완료되었습니다.')
            return redirect('register_done')  # 회원가입 후 로그인 페이지로 리다이렉션
    else:
        form = RegisterForm()
    return render(request, 'REG.html', {'form': form})

def register_done(request):
    return render(request, 'REG_DONE.html')

def find_id(request):
    if request.method == 'POST':
        form = FindIDForm(request.POST)
        if form.is_valid():
            user = User.objects.get(
                first_name=form.cleaned_data['first_name'],
                email=form.cleaned_data['email']
            )
            request.session['found_user_id'] = user.id  
            return redirect('find_id_result')  
    else:
        form = FindIDForm()
    
    return render(request, 'FND_ID.html', {'form': form})

def find_id_result(request):
    user_id = request.session.get('found_user_id') 
    if not user_id:
        return redirect('find_id')  

    found_user = get_object_or_404(User, id=user_id)
    
    return render(request, 'FND_ID_RESULT.html', {'found_user': found_user})


def find_passwd(request):
    if request.method == 'POST':
        form = FindPasswordForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(username=username, first_name=first_name, email=email)
                request.session['reset_user_id'] = user.id
                return redirect('reset_passwd')
            except User.DoesNotExist:
                form.add_error(None, "입력한 정보와 일치하는 사용자가 없습니다.")
    else:
        form = FindPasswordForm()

    return render(request, 'FND_PW.html', {'form': form})

def reset_passwd(request):
    user_id = request.session.get('reset_user_id')
    if not user_id:
        return redirect('find_passwd')  # 세션에 사용자가 없으면 비밀번호 찾기 페이지로 리다이렉션
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = PasswordResetConfirmForm(request.POST, user=user)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  # 세션 업데이트
            request.session.pop('reset_user_id', None)  # 세션에서 사용자 ID 제거
            return redirect('reset_passwd_done')  # 비밀번호 재설정 완료 후 리다이렉션
    else:
        form = PasswordResetConfirmForm(user=user)
    
    return render(request, 'FND_PW_RESULT.html', {'form': form})

def reset_passwd_done(request):
    return render(request, 'FND_PW_DONE.html')

def user_profile(request):
    return render(request, 'USR.html', {'user': request.user})

def search_products(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'SER.html', {'results': results, 'query': query})