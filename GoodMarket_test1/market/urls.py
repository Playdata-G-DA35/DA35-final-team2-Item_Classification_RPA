from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import add_product, save_selected_image, find_image

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('product/<int:product_id>/delete/', views.delete_product, name='product_delete'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('chat/<int:product_id>/', views.chat, name='chat'),  
    path('chat/', views.chat_view, name='chat_view'),  
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('profile/', views.user_profile, name='user_profile'),
    path('search/', views.search_products, name='search_products'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_id/result/', views.find_id, name='find_id_result'),
    path('find_passwd/', views.find_passwd, name='find_passwd'),
    path('reset_passwd/', views.reset_passwd, name='reset_passwd'),
    path('reset_passwd/done/', views.reset_passwd_done, name='reset_passwd_done'),
    path('save-selected-image/', save_selected_image, name='save_selected_image'),  # Ensure this line exists
    path('find-image/', find_image, name='find_image'),  # Add this line for findimage.html
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
