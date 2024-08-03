from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('product/upload/', views.product_upload, name='product_upload'),
    path('product_x/<int:product_x_id>/', views.product_x_detail, name='product_x_detail'),
]
