# Generated by Django 4.2.15 on 2024-08-22 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0002_alter_product_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckFile',
            fields=[
                ('check_file_id', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to='check_files/')),
                ('file_reg_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductCheck',
            fields=[
                ('product_check_id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='product_checks/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='ProductX',
        ),
        migrations.AddField(
            model_name='checkfile',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='market.productcheck'),
        ),
    ]
