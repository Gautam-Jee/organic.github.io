# Generated by Django 4.0.2 on 2022-05-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='order',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]