from django import forms
from .models import Product, ProductFile, ProductX

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'user', 'name', 'price', 'description']

class ProductFileForm(forms.ModelForm):
    class Meta:
        model = ProductFile
        fields = [ 'file']  #'file_name',

class ProductXForm(forms.ModelForm):
    class Meta:
        model = ProductX
        fields = ['file']
