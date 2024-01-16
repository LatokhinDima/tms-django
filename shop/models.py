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
   user = models.OneToOneField(User, on_delete=models.CASCADE)
   shopping_cart = models.OneToOneField('Order', on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='+')

   def __str__(self):
        return self.user

class OrderEntry(models.Model):
    product = models.ForeignKey(Product, related_name='product', on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    order = models.ForeignKey('Order', related_name='order_entries', on_delete=models.CASCADE)

    def __str__(self):
        return self.product


class Order(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='INITIAL')




