# Generated by Django 3.2.8 on 2023-09-22 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vendor',
            name='location',
        ),
        migrations.RemoveField(
            model_name='vendor',
            name='views',
        ),
        migrations.AlterField(
            model_name='vendor',
            name='vendor_image',
            field=models.ImageField(default='images/site_images/vendor-dummy.jpg', help_text='Upload a your image', upload_to='images/uploads/vendor/', verbose_name='profile image'),
        ),
    ]
