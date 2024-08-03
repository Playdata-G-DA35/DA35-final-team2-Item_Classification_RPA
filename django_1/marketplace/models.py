from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    account_id = models.CharField(max_length=30, unique=True)
    user_pwd = models.CharField(max_length=128)  # Password hashing is handled separately
    user_name = models.CharField(max_length=50)
    user_email = models.EmailField(max_length=100, unique=True)
    user_reg_date = models.DateTimeField(auto_now_add=True)
    user_auth = models.CharField(max_length=10, choices=[('USER', 'User'), ('ADMIN', 'Admin')])

    def __str__(self):
        return self.account_id

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
    product_file = models.AutoField(primary_key=True)
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
