from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL,
                                null=True, blank=True, default=None)
    shopping_cart = models.OneToOneField('Order', on_delete=models.SET_NULL,
                                         null=True, blank=True, related_name='+')

    def __str__(self):
        return str(self.user)


class OrderEntry(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='+')
    count = models.IntegerField(default=0)
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_entries')

    def __str__(self):
        return f'{self.product} - {self.count}'


class Status(models.TextChoices):
    INITIAL = 'INITIAL', 'Initial'
    COMPLETED = 'COMPLETED', 'Completed'
    DELIVERED = 'DELIVERED', 'Delivered'


class Order(models.Model):
    class Status(models.TextChoices):
        INITIAL = 'INITIAL', 'Initial'
        COMPLETED = 'COMPLETED', 'Completed'
        DELIVERED = 'DELIVERED', 'Delivered'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INITIAL)

    def __str__(self):
        return f'{self.profile} - {self.status}'

    def get_total_price(self):
        return sum(order_entry.product.price * order_entry.count for order_entry in self.order_entries.all())

    def get_products_count(self):
        return sum(order_entry.count for order_entry in self.order_entries.all())

    def get_order_status(self):
        if self.status == Status.INITIAL:
            return 'INITIAL'
        elif self.status == Status.COMPLETED:
            return 'COMPLETED'
        elif self.status == Status.DELIVERED:
            return 'DELIVERED'
        else:
            return 'UNKNOWN'
