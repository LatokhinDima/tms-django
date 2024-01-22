from django.contrib import admin
from .models import Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'price', 'category']
    search_fields = ['name']
    list_filter = ['name', 'price', 'category']

admin.site.register(Product, ProductAdmin)


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    fields = ['name', 'description', 'price']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    list_filter = ['name']
    inlines = [ProductInline]

admin.site.register(Category, CategoryAdmin)


