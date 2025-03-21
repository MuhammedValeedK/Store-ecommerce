from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from ecommerceapp.models import Cart, Wishlist






class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    User.add_to_class('get_wishlist_products', lambda user: [wishlist_item.product for wishlist_item in Wishlist.objects.filter(user=user)])
    def __str__(self):
        return f"{self.user.username}'s Profile"
    def get_cart(self):
        return Cart.objects.filter(user=self.user)
    


