from django.contrib.auth.models import User
from django.db import models

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
    price = models.DecimalField(max_digits=10, decimal_places=0)
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
    
    # New foreign key to check2 model
    check2_image = models.ForeignKey('check2', on_delete=models.SET_NULL, null=True, blank=True, related_name='product_files')

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

class ProductCheck(models.Model):
    product_check_id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='product_checks/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image {self.product_check_id}'

class check2(models.Model):
    image = models.ImageField(upload_to='check2_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Check2 Image {self.id}"

# models.py
from django.db import models

class FinalModel(models.Model):
    image = models.ImageField(upload_to='final_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.image.name

# models.py
from django.db import models

class FindImage(models.Model):
    image = models.ImageField(upload_to='find_images/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"FindImage {self.id} - {self.created_at}"
