# Generated by Django 5.0 on 2024-01-12 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]