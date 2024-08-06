# market/admin.py

from django.contrib import admin
from .models import User, Category, Product, ProductFile, ProductX, Chat

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductFile)
admin.site.register(ProductX)
admin.site.register(Chat)
