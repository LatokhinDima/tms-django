from django.contrib import admin
from .models import Category, Product, Profile, Order, OrderEntry

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderEntry)
