# Generated by Django 4.0.2 on 2022-05-21 00:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0021_alter_order_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productsseller',
            name='seller_state',
            field=models.CharField(max_length=100),
        ),
    ]
