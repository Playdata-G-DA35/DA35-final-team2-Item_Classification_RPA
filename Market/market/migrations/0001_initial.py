# Generated by Django 5.0.7 on 2024-08-06 00:20

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_name', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('account_id', models.CharField(max_length=30, unique=True)),
                ('user_pwd', models.CharField(max_length=128)),
                ('user_name', models.CharField(max_length=50)),
                ('user_email', models.EmailField(max_length=100, unique=True)),
                ('user_reg_date', models.DateTimeField(auto_now_add=True)),
                ('user_auth', models.CharField(choices=[('USER', 'User'), ('ADMIN', 'Admin')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField()),
                ('reg_date', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='market.user')),
            ],
        ),
        migrations.CreateModel(
            name='ProductFile',
            fields=[
                ('product_file', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='product_files/')),
                ('file_reg_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='market.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductX',
            fields=[
                ('product_x_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='reversed_product_files/')),
                ('file_reg_date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reversed_files', to='market.product')),
            ],
        ),
    ]
