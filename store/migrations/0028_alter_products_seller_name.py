# Generated by Django 4.0.2 on 2022-05-22 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0027_remove_products_description_products_seller_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='seller_name',
            field=models.CharField(default='Fresh and Nutritious with good packaging', max_length=200),
        ),
    ]
