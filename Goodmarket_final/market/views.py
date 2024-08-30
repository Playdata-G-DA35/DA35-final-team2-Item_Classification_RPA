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


from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import os
import glob
import torch
from torchvision import transforms
import torchvision.models as models
import torch.nn as nn
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from .models import Product, ProductFile, check2, FinalModel
from .forms import ProductForm, ProductCheckForm
from django.conf import settings
from .category import ImageEmbeddingModel
from django.http import JsonResponse
from urllib.parse import unquote

# 모델 정보 딕셔너리 정의
model_info_dict = {
    "onepiece": [r"C:\Users\USER\Desktop\GoodMarket_test\059.pth", 3]
    # 필요한 다른 카테고리와 모델 정보를 추가
}

@login_required
def add_product(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        product_check_form = ProductCheckForm(request.POST, request.FILES)
        
        selected_image_url = request.POST.get('selected_image_url', None)

        if 'imcheck' in request.POST:
            if product_check_form.is_valid():
                product_check = product_check_form.save()
                messages.success(request, '이미지가 성공적으로 저장되었습니다.')

                my_datapath = os.path.join(settings.MEDIA_ROOT, 'product_checks')
                files = glob.glob(os.path.join(my_datapath, '*'))
                latest_file = max(files, key=os.path.getmtime)
                
                output_dir = os.path.join(settings.MEDIA_ROOT)
                os.system(f"python detect_clothes/detect.py --source \"{latest_file}\" --project \"{output_dir}\"")

                crops_dir = os.path.join(settings.MEDIA_ROOT, 'test', 'crops')
                image_files = glob.glob(os.path.join(crops_dir, '**', '*.*'), recursive=True)
                
                for image_file in image_files:
                    result_image_name = os.path.relpath(image_file, start=settings.MEDIA_ROOT)
                    
                    if not check2.objects.filter(image=result_image_name).exists():
                        check2.objects.create(image=result_image_name)
            
            return redirect('add_product')

        elif 'selected_image_url' in request.POST:
            if product_form.is_valid() and selected_image_url:
                product = product_form.save(commit=False)
                product.user = request.user
                product.save()
                messages.success(request, '상품이 성공적으로 등록되었습니다.')

                try:
                    # 선택된 이미지의 경로를 처리합니다.
                    if selected_image_url.startswith('/media/'):
                        relative_path = selected_image_url[len('/media/'):]
                    else:
                        relative_path = selected_image_url

                    # FinalModel에서 선택된 이미지를 가져옵니다.
                    final_image = FinalModel.objects.get(image=relative_path)
                    file_path = os.path.join(settings.MEDIA_ROOT, final_image.image.name)
                    
                    if not os.path.exists(file_path):
                        raise FileNotFoundError('파일이 존재하지 않습니다.')

                    # 카테고리 추출
                    cate_big = "onepiece"  # 예시 카테고리, 실제로는 적절한 카테고리로 수정
                    base_model = ImageEmbeddingModel(
                        weight_path=model_info_dict[cate_big][0], 
                        class_num=model_info_dict[cate_big][1], 
                        img_path=file_path
                    )
                    category = base_model.get_category()
                    max_value, max_index = torch.max(category, dim=1)
                    category_label = max_index.item()

                    with default_storage.open(final_image.image.name, 'rb') as f:
                        content = ContentFile(f.read(), os.path.basename(final_image.image.name))
                        product_file = ProductFile(
                            product=product,
                            file_name=os.path.basename(final_image.image.name),
                            check2_image=None  # 관계 설정을 생략
                        )
                        product_file.file.save(os.path.basename(final_image.image.name), content)
                        product_file.save()

                    messages.success(request, f'이미지가 성공적으로 저장되었습니다. 카테고리: {category_label}')

                except FinalModel.DoesNotExist:
                    messages.error(request, '선택한 이미지가 데이터베이스에 존재하지 않습니다.')
                    return redirect('add_product')

                return redirect('home')

    else:
        product_form = ProductForm()
        product_check_form = ProductCheckForm()

    now = timezone.now()
    five_seconds_ago = now - timedelta(seconds=5)
    recent_images = check2.objects.filter(created_at__gte=five_seconds_ago)

    return render(request, 'ADD.html', {
        'product_form': product_form,
        'product_check_form': product_check_form,
        'recent_images': recent_images,
    })

def save_selected_image(request):
    if request.method == 'POST':
        image_url = request.POST.get('image_url')
        if image_url:
            try:
                # URL 디코딩 (예: %20 -> 공백)
                decoded_image_url = unquote(image_url)
                
                if decoded_image_url.startswith('/media/'):
                    relative_path = decoded_image_url[len('/media/'):]
                else:
                    relative_path = decoded_image_url

                final_image = FinalModel(image=relative_path)
                final_image.save()

                file_path = os.path.join(settings.MEDIA_ROOT, final_image.image.name)

                if not os.path.exists(file_path):
                    raise FileNotFoundError(f'파일이 존재하지 않습니다: {file_path}')

                cate_big = "onepiece"
                base_model = ImageEmbeddingModel(
                    weight_path=model_info_dict[cate_big][0], 
                    class_num=model_info_dict[cate_big][1], 
                    img_path=file_path
                )
                category = base_model.get_category()
                max_value, max_index = torch.max(category, dim=1)
                category_label = max_index.item()

                response_data = {'success': True, 'message': 'Image saved successfully', 'category': category_label}
                
                # 디버깅용 출력
                print(f"Response Data: {response_data}")
                
                return JsonResponse(response_data)
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})
        else:
            return JsonResponse({'success': False, 'message': 'No image URL provided'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# views.py
import os
import glob
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse  # reverse 함수 임포트
from .chromafind import find_similar_images
from .models import ProductFile, Product, FindImage

def find_image(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('image_file')
        if uploaded_file:
            # 이미지 파일 모델에 저장
            find_image_instance = FindImage(image=uploaded_file)
            find_image_instance.save()

            # 저장된 파일 경로
            file_path = os.path.join(settings.MEDIA_ROOT, find_image_instance.image.name)

            try:
                # 1. YOLO 모델을 사용하여 업로드된 이미지 크롭
                output_dir = os.path.join(settings.MEDIA_ROOT, 'cropped_images')
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

                os.system(f"python detect_clothes/detect.py --source \"{file_path}\" --project \"{output_dir}\" --save-txt --save-conf")

                # 2. 업로드된 이미지에 대해서만 크롭된 이미지 파일 경로 찾기 (5초 이내)
                now = datetime.now()
                five_seconds_ago = now - timedelta(seconds=5)
                
                cropped_image_files = []
                for img_file in glob.glob(os.path.join(output_dir, '**', '*.*'), recursive=True):
                    # 이미지 파일의 수정 시간을 가져와 5초 이내인지 확인
                    file_mtime = datetime.fromtimestamp(os.path.getmtime(img_file))
                    if file_mtime > five_seconds_ago:
                        # 'crops' 디렉토리 하위의 이미지 파일만 필터링
                        if '/crops/' in img_file.replace("\\", "/"):
                            cropped_image_files.append(img_file)

                if not cropped_image_files:  # 크롭된 이미지가 없을 때 처리
                    return JsonResponse({'success': True, 'cropped_images': []})

                # 크롭된 이미지들을 클라이언트에게 전송
                cropped_image_urls = [os.path.relpath(img, start=settings.MEDIA_ROOT).replace("\\", "/") for img in cropped_image_files]
                return JsonResponse({'success': True, 'cropped_images': cropped_image_urls})

            except Exception as e:
                # 에러 발생 시 에러 메시지 반환
                return JsonResponse({'success': False, 'message': str(e)})
            finally:
                # 원본 이미지 파일 삭제 (선택 사항)
                if os.path.exists(file_path):
                    os.remove(file_path)

    return render(request, 'findimage.html')


def search_similar_images(request):
    if request.method == 'POST':
        clicked_image_url = request.POST.get('image_url')
        if clicked_image_url:
            file_path = os.path.join(settings.MEDIA_ROOT, clicked_image_url)
            
            try:
                # 유사 이미지 검색
                model_info_dict = {
                    "onepiece": [r"C:\Users\USER\Desktop\GoodMarket_test\059.pth", 3]
                }
                similar_images = find_similar_images(file_path, "onepiece", model_info_dict, top_k=8)

                results = []
                for similarity, product_file_id in similar_images:
                    try:
                        product_file = ProductFile.objects.get(product_file_id=product_file_id)
                        product = product_file.product
                        results.append({
                            'id': product_file.file.name,
                            'score': similarity,
                            'product_name': product.name,
                            'product_price': product.price,
                            'product_description': product.description,
                            'product_image_url': product_file.file.url,
                            'product_detail_url': request.build_absolute_uri(reverse('product_detail', args=[product.product_id]))
                        })
                    except ProductFile.DoesNotExist:
                        continue

                return JsonResponse({'success': True, 'results': results})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request method'})
