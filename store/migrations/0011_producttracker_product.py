# Generated by Django 4.0.2 on 2022-05-13 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_producttracker'),
    ]

    operations = [
        migrations.AddField(
            model_name='producttracker',
            name='product',
            field=models.CharField(default='', max_length=200),
        ),
    ]
