# Generated by Django 3.2.8 on 2023-06-30 07:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_name', models.CharField(max_length=255, unique=True)),
                ('unique_id', models.CharField(max_length=50, unique=True)),
                ('vendor_image', models.ImageField(default='images/others/igor-lypnytskyi-PobecUzsK4c-unsplash.png', help_text='Upload a your image', upload_to='images/uploads/profile/', verbose_name='profile image')),
                ('is_active', models.BooleanField(default=True)),
                ('views', models.IntegerField(default=0, editable=False, verbose_name='Restaurant was visited')),
                ('location', models.CharField(default='No Address', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='which_vendor', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'List of Vendors',
                'ordering': ['store_name'],
            },
        ),
    ]