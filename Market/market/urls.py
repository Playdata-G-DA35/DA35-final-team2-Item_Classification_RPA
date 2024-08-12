# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('product_x/<int:product_x_id>/', views.product_x_detail, name='product_x_detail'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('sell/', views.sell_product, name='sell_product'),
    path('chat/', views.chat, name='chat'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('profile/', views.user_profile, name='user_profile'),
    path('search/', views.search_products, name='search_products'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_id/result/', views.find_id_result, name='find_id_result'),
    path('find_passwd/', views.find_passwd, name='find_passwd'),
    path('reset_passwd/', views.reset_passwd, name='reset_passwd'),
    path('reset_passwd/done/', views.reset_passwd_done, name='reset_passwd_done'),
]
