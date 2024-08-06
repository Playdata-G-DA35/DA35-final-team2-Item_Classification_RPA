# market/views.py

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, ProductX, ProductFile

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

def login(request):
    # Implement this view
    return render(request, 'LOG.html')

def register(request):
    # Implement this view
    return render(request, 'REG.html')

def user_profile(request):
    # Implement this view
    return render(request, 'USR.html')

def search_products(request):
    query = request.GET.get('q')
    results = Product.objects.filter(name__icontains=query) if query else []
    return render(request, 'SER.html', {'results': results, 'query': query})
