# Generated by Django 5.0 on 2024-01-26 08:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_alter_orderentry_order_alter_profile_shopping_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='shopping_cart',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='shopping_cart', to='shop.order'),
        ),
    ]