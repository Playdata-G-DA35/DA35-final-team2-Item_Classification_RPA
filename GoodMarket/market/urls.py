# market/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('product_x/<int:product_x_id>/', views.product_x_detail, name='product_x_detail'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('sell/', views.sell_product, name='sell_product'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('search/', views.search_products, name='search_products'),
]
