# views.py
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductX, ProductFile, Chat, Category
from .forms import RegisterForm, FindIDForm, FindPasswordForm, PasswordResetConfirmForm, ProductForm, ProductFileForm
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def file_detail(request, file_id):
    file = get_object_or_404(ProductFile, product_file=file_id)
    return render(request, 'PRD.html', {'file': file})

def product_x_detail(request, product_x_id):
    file = get_object_or_404(ProductX, product_x_id=product_x_id)
    return render(request, 'PRD.html', {'file': file})

def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'product': product})

def sell_product(request):
    # Implement this view
    return render(request, 'ADD.html')

def chat(request):
    # Implement this view
    return render(request, 'CHT.html')

def login_view(request):
    next_url = request.POST.get('next') or request.GET.get('next', 'home')  # 기본값으로 'home' 설정

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)  # 로그인 성공 후 리다이렉션
        else:
            messages.error(request, '아이디 또는 비밀번호가 잘못되었습니다.')
    else:
        form = AuthenticationForm()

    return render(request, 'LOG.html', {'form': form, 'next': next_url})

def logout_view(request):
    logout(request)
    return redirect('home') # 로그아웃 후 홈 페이지로 리다이렉션

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
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
                first_name = form.cleaned_data['first_name'],
                email = form.cleaned_data['email']
            )
            return render(request, 'FND_ID_RESULT.html', {'user': user})
    else:
        form = FindIDForm()

    return render(request, 'FND_ID.html', {'form': form})

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

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        
        if product_form.is_valid():
            product = product_form.save(commit=False)
            product.user = request.user
            product.save()

            files = request.FILES.getlist('file')
            for file in files:
                ProductFile.objects.create(product=product, file_name=file.name, file=file)

            return redirect('home')  # 홈 페이지로 리디렉션

    else:
        product_form = ProductForm()

    return render(request, 'ADD.html', {
        'product_form': product_form,
    })


def home(request):
    products = Product.objects.all()
    # 각 제품에 대해 첫 번째 파일을 추가합니다.
    for product in products:
        product.first_file = product.files.first()  # 각 제품에 파일을 추가합니다.

    return render(request, 'HOM.html', {'products': products})

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    # 특정 상품과 관련된 첫 번째 파일을 가져옵니다.
    product_file = product.files.first()  # 'files'는 ProductFile 모델의 related_name
    return render(request, 'product_detail.html', {'product': product, 'product_file': product_file})

@login_required
def user_profile(request):
    user = request.user
    products = Product.objects.filter(user=user)
    product_files = ProductFile.objects.filter(product__in=products)
    return render(request, 'USR.html', {'user': user, 'products': products, 'product_files': product_files})

@login_required
def chat(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    # Prevent the user from accessing the chat if they own the product
    if product.user == request.user:
        return redirect('home')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            Chat.objects.create(
                product=product,
                sender=request.user,
                receiver=product.user,
                message=message,
                timestamp=timezone.now()
            )
            return redirect('chat', product_id=product_id)

    chats = Chat.objects.filter(product=product).order_by('timestamp')
    return render(request, 'CHT.html', {'product': product, 'chats': chats})

@login_required
def chat_view(request):
    user = request.user
    products = Product.objects.filter(user=user)

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        message = request.POST.get('message')

        if product_id and message:
            product = get_object_or_404(Product, pk=product_id, user=user)
            Chat.objects.create(
                product=product,
                sender=user,
                receiver=product.chats.exclude(sender=user).first().sender,  # 구매자
                message=message,
                timestamp=timezone.now()
            )
            return redirect('chat_view')  # 메시지를 보낸 후 페이지를 새로 고침

    return render(request, 'chat_view.html', {'products': products})
