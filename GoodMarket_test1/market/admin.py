# market/admin.py

from django.contrib import admin
from .models import User, Category, Product, ProductFile,  Chat, ProductCheck, check2, FinalModel

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(ProductFile)
admin.site.register(Chat)
admin.site.register(ProductCheck)
admin.site.register(check2)
admin.site.register(FinalModel)

