# urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('file/<int:file_id>/', views.file_detail, name='file_detail'),
    path('product/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add/', views.add_product, name='add_product'),
    path('find_image/', views.find_image, name='find_image'),
    path('save_selected_image/', views.save_selected_image, name='save_selected_image'),
    path('chat/<int:product_id>/', views.chat, name='chat'),  
    path('chat/', views.chat_view, name='chat_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('register/done/', views.register_done, name='register_done'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('search/', views.search_products, name='search_products'),
    path('find_id/', views.find_id, name='find_id'),
    path('find_id/result/', views.find_id, name='find_id_result'),
    path('find_passwd/', views.find_passwd, name='find_passwd'),
    path('reset_passwd/', views.reset_passwd, name='reset_passwd'),
    path('reset_passwd/done/', views.reset_passwd_done, name='reset_passwd_done'),
    path('<str:category_name>/', views.category_products, name='category_products'),
    path('<str:category_name>/sort/<str:sort_by>/', views.category_products, name='sorted_category_products'),
    path('<str:category_name>/<str:subcategory_name>/', views.subcategory_products, name='subcategory_products'),
    path('<str:category_name>/<str:subcategory_name>/sort/<str:sort_by>/', views.subcategory_products, name='sorted_subcategory_products'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
