# Generated by Django 4.0.2 on 2022-05-16 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_remove_order_seller'),
    ]

    operations = [
        migrations.AddField(
            model_name='productssellerfarmer',
            name='image',
            field=models.ImageField(default='', upload_to='store/images/'),
        ),
    ]
