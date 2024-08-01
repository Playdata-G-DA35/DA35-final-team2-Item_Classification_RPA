from django import forms
from .models import Product, ProductFile

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'user', 'name', 'price', 'description']

class ProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = ['file_name', 'file']
