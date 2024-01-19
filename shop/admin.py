from django.contrib import admin
from .models import Category, Product, Profile, Order, OrderEntry

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['name']})
    ]

    inlines = [ProductInline]

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Profile)
admin.site.register(Order)
admin.site.register(OrderEntry)
