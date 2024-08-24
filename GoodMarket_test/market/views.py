# views.py
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductFile, Chat, Category
from .forms import RegisterForm, FindIDForm, FindPasswordForm, PasswordResetConfirmForm, ProductForm, ProductFileForm
from django.urls import path
from django.contrib.auth.decorators import login_required
from django.utils import timezone

def file_detail(request, file_id):
    file = get_object_or_404(ProductFile, product_file=file_id)
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

'''
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
'''

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
            return redirect('chat_view')  # 메시지를 보낸 후 페이지를 새로 고침   --project media"

    return render(request, 'chat_view.html', {'products': products})

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProductForm, ProductCheckForm
from .models import ProductCheck
import os
import glob


import os
import glob
from django.conf import settings
from .models import check2
from .forms import ProductForm, ProductCheckForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        product_check_form = ProductCheckForm(request.POST, request.FILES)
        
        if 'imcheck' in request.POST:
            if product_check_form.is_valid():
                product_check = product_check_form.save()
                messages.success(request, '이미지가 성공적으로 저장되었습니다.')
                
                # 디렉토리 내 모든 파일의 경로를 가져옵니다.
                my_datapath = os.path.join(settings.MEDIA_ROOT, 'product_checks')
                files = glob.glob(os.path.join(my_datapath, '*'))
                latest_file = max(files, key=os.path.getmtime)
                
                # YOLO 모델을 실행하여 이미지를 처리합니다.
                output_dir = os.path.join(settings.MEDIA_ROOT)  # 'test' 없음
                os.system(f"python detect_clothes/detect.py --source \"{latest_file}\" --project \"{output_dir}\"")

                # crops 폴더 내 모든 이미지 파일 경로를 가져옵니다.
                crops_dir = os.path.join(settings.MEDIA_ROOT, 'test', 'crops')
                image_files = glob.glob(os.path.join(crops_dir, '**', '*.*'), recursive=True)
                
                for image_file in image_files:
                    # YOLO 결과 이미지 경로를 상대 경로로 설정합니다.
                    result_image_name = os.path.relpath(image_file, start=settings.MEDIA_ROOT)
                    
                    # check2 모델에서 해당 이미지가 이미 존재하는지 확인
                    if not check2.objects.filter(image=result_image_name).exists():
                        # check2 모델에 이미지 저장
                        check2.objects.create(image=result_image_name)
                
                # YOLO 처리 후 원본 파일 삭제
                for file in files:
                    os.remove(file)

                return redirect('check')  # 체크 페이지로 리디렉션

    else:
        product_form = ProductForm()
        product_check_form = ProductCheckForm()
    
    return render(request, 'ADD.html', {
        'product_form': product_form,
        'product_check_form': product_check_form,
    })



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import check2

@login_required
def check(request):
    # 현재 시간
    now = timezone.now()
    # 최근 5초
    five_seconds_ago = now - timedelta(seconds=5)
    # 최근 5초 동안 추가된 이미지
    images = check2.objects.filter(created_at__gte=five_seconds_ago)
    return render(request, 'check.html', {'images': images})

# views.py

from django.http import JsonResponse
import subprocess

def process_image(request):
    # 이미지 경로를 GET 파라미터로 받습니다
    image_path = request.GET.get('image_path')
    
    # test_import.py를 호출하여 이미지 처리
    if image_path:
        try:
            # Python 스크립트를 호출합니다
            result = subprocess.run(
                ['python', 'test_import.py', image_path],
                capture_output=True,
                text=True
            )
            # 터미널 출력 결과를 로그로 남깁니다
            print(result.stdout)
            print(result.stderr)
            output = result.stdout
        except Exception as e:
            output = f"Error occurred: {e}"
    else:
        output = "No image path provided."
    
    return JsonResponse({'result': output})


# views.py

from django.http import JsonResponse
from django.core.files.storage import default_storage
import subprocess
import os

def process_image(request):
    image_path = request.GET.get('image_path')
    
    if image_path:
        # 웹 경로를 실제 파일 시스템 경로로 변환
        full_path = default_storage.path(image_path)
        
        if os.path.exists(full_path):
            try:
                # test_import.py를 호출하여 이미지 처리
                result = subprocess.run(
                    ['python', 'test_import.py', full_path],
                    capture_output=True,
                    text=True
                )
                # 서버 로그(터미널)에 출력
                print(result.stdout)
                print(result.stderr)
                output = result.stdout
            except Exception as e:
                output = f"Error occurred: {e}"
        else:
            output = "File not found."
    else:
        output = "No image path provided."
    
    # 클라이언트에게 처리 결과 반환
    return JsonResponse({'result': output})
