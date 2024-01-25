from django.contrib.auth.models import User

from .models import Order, Profile
from django.db.models.signals import post_save
from django.dispatch import receiver


#@receiver(post_save, sender=User)
#def create_profile(instance: User, created: bool, **kwargs):
#    if created:
#        instance.profile = Profile.objects.create(user=instance)
#        instance.save()


#@receiver(post_save, sender=Profile)
#def create_shopping_cart(instance: Profile, created: bool, **kwargs):
#    if created:
#        instance.shopping_cart = Order.objects.create(profile=instance)
#        instance.save()
