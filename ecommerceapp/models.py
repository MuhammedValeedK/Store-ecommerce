from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Contact(models.Model):
    # contact_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

    def __int__(self):
        return self.id

class Slider(models.Model):
    title = models.CharField(max_length=100)  # Title text
    subtitle = models.CharField(max_length=200, blank=True)  # Optional subtitle
    image = models.ImageField(upload_to='sliders/')  # Image for the slider
    button_text = models.CharField(max_length=50, blank=True)  # Button text
    button_link = models.URLField(blank=True)  # Button URL
    order = models.PositiveIntegerField(default=0)  # To control display order

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['order']


from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default="fa-box")  # Default FontAwesome icon
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(unique=True, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # Use ForeignKey
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.product_name






class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for {self.user.username}"

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to the product
    added_on = models.DateTimeField(auto_now_add=True)  # Timestamp when the item was added

    class Meta:
        unique_together = ('user', 'product')  # Ensure each product is added only once per user

    def __str__(self):
        return f"{self.user.username}'s Wishlist: {self.product.product_name}"







class Orders(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    amount = models.FloatField(default=0)
    email = models.CharField(max_length=111)
    address1 = models.CharField(max_length=111)
    address2 = models.CharField(max_length=111, blank=True, null=True)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=111)
    zip_code = models.CharField(max_length=111)
    phone = models.CharField(max_length=111, default="")
    payment_method = models.CharField(max_length=50, default="COD")  
    payment_status = models.CharField(max_length=50, default="Pending") 
    def __str__(self):
        return f"Order {self.id} by {self.name}"


class OrderUpdate(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True, blank=True)  # ✅ Allow null values temporarily
    update_id = models.AutoField(primary_key=True)
    
    update_desc = models.CharField(max_length=5000)
    delivered = models.BooleanField(default=False)
    payment_status = models.CharField(max_length=50, default="Pending")  # New field for payment status
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."






