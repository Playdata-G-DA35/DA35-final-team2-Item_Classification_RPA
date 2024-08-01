
# 현재 user와 카테고리가 없어서 임시방편
from django.db import migrations

def add_initial_data(apps, schema_editor):
    Category = apps.get_model('marketplace', 'Category')
    User = apps.get_model('marketplace', 'User')

    Category.objects.get_or_create(name='가전제품')
    User.objects.get_or_create(
        account_id='testuser',
        user_pwd='testpassword',  # 비밀번호는 실제로 해싱되어야 합니다
        user_name='이상준',
        user_email='testuser@example.com'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),  # 이전 마이그레이션 파일로 대체
    ]

    operations = [
        migrations.RunPython(add_initial_data),
    ]
