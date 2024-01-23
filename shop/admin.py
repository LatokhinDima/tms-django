from django.contrib import admin
from .models import Category, Product, Profile, Order, OrderEntry
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


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


class ProfileInline(admin.StackedInline):
    model = Profile


class MyUserAdmin(UserAdmin):
    inlines = [ProfileInline]


admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['profile', 'status']
    list_filter = ['status']


admin.site.register(Order, OrderAdmin)


class OrderEntryAdmin(admin.ModelAdmin):
    list_display = ['product', 'count', 'order']
    list_filter = ['order']


admin.site.register(OrderEntry, OrderEntryAdmin)
