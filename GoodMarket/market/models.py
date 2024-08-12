from django.contrib.auth.models import User  # Django 기본 User 모델 가져오기
from django.db import models
from django.utils import timezone

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Django 기본 User 모델 참조
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductFile(models.Model):
    product_file_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='files')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='product_files/')
    file_reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class ProductX(models.Model):
    product_x_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reversed_files')
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to='reversed_product_files/')
    file_reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file_name

class Chat(models.Model):
    room_name = models.CharField(max_length=255)
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'[{self.timestamp}] {self.room_name}: {self.message}'
