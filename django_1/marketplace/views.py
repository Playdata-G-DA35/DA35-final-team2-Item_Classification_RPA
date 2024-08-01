from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Product, ProductFile
from .forms import ProductForm, ProductFileForm

def product_upload(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        ProductFileFormSet = modelformset_factory(ProductFile, form=ProductFileForm, extra=3)  # extra=3는 기본적으로 3개의 빈 폼을 생성
        file_formset = ProductFileFormSet(request.POST, request.FILES, queryset=ProductFile.objects.none())
        
        if product_form.is_valid() and file_formset.is_valid():
            product = product_form.save()
            for form in file_formset:
                if form.cleaned_data.get('file'):  # 파일이 있는 경우만 저장
                    file = form.save(commit=False)
                    file.product = product
                    file.save()
            return redirect('home')  # 성공적으로 저장한 후 리디렉션
            
    else:
        product_form = ProductForm()
        ProductFileFormSet = modelformset_factory(ProductFile, form=ProductFileForm, extra=3)  # extra=3는 기본적으로 3개의 빈 폼을 생성
        file_formset = ProductFileFormSet(queryset=ProductFile.objects.none())
    
    return render(request, 'product_upload.html', {'product_form': product_form, 'file_formset': file_formset})

def home(request):
    # 모든 상품과 관련된 파일을 가져옴
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})

def file_detail(request, file_id):
    # 특정 파일을 가져와서 상세 정보 페이지로 렌더링
    file = get_object_or_404(ProductFile, product_file=file_id)
    return render(request, 'buy.html', {'file': file})