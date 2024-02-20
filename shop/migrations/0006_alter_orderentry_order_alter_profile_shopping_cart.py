# Generated by Django 5.0 on 2024-01-25 19:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_order_status_alter_profile_shopping_cart_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderentry',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='entries', to='shop.order'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='shopping_cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shopping_cart', to='shop.order'),
        ),
    ]
