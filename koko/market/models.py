# market/models.py

from django.contrib.auth.models import User
from django.db import models
from PIL import Image

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # 이미지 크기 조정
        if self.file and self.file.name.lower().endswith(('png', 'jpg', 'jpeg')):
            img = Image.open(self.file.path)
            if img.height > 640 or img.width > 640:
                output_size = (640, 640)
                img.thumbnail(output_size)
                img.save(self.file.path)

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
    chat_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chats')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_chats')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_chats')
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Chat between {self.sender.username} and {self.receiver.username} about {self.product.name}'
