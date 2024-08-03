from django.shortcuts import render, redirect, get_object_or_404
from django.forms import modelformset_factory
from .models import Product, ProductFile, ProductX
from .forms import ProductForm, ProductFileForm, ProductXForm
from .test import reverse_image  # 이미지 처리 모듈


def product_upload(request):
    if request.method == 'POST':
        product_form = ProductForm(request.POST)
        ProductFileFormSet = modelformset_factory(ProductFile, form=ProductFileForm, extra=3)
        file_formset = ProductFileFormSet(request.POST, request.FILES, queryset=ProductFile.objects.none())

        if product_form.is_valid() and file_formset.is_valid():
            product = product_form.save()
            for form in file_formset:
                if form.cleaned_data.get('file'):
                    file = form.save(commit=False)
                    file.product = product
                    file.save()
                    
                    # 이미지 좌우 반전 처리 및 ProductX 저장
                    reversed_file_path = reverse_image(file.file.path)
                    ProductX.objects.create(
                        product=product,
                        file_name=f'reversed_{file.file_name}',
                        file=reversed_file_path
                    )

            return redirect('home')
    else:
        product_form = ProductForm()
        ProductFileFormSet = modelformset_factory(ProductFile, form=ProductFileForm, extra=3)
        file_formset = ProductFileFormSet(queryset=ProductFile.objects.none())

    return render(request, 'product_upload.html', {'product_form': product_form, 'file_formset': file_formset})


def home(request):
    products = Product.objects.all()
    reversed_files = ProductX.objects.all()
    return render(request, 'home.html', {'products': products, 'reversed_files': reversed_files})

def file_detail(request, file_id):
    # 특정 파일을 가져와서 상세 정보 페이지로 렌더링
    file = get_object_or_404(ProductFile, product_file=file_id)
    return render(request, 'buy.html', {'file': file})

def product_x_detail(request, product_x_id):
    file = get_object_or_404(ProductX, product_x_id=product_x_id)
    return render(request, 'product_x.html', {'file': file})