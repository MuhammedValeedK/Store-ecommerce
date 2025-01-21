from django.db import models
from django.conf import settings







class Contact(models.Model):
    # contact_id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    email=models.EmailField()
    desc=models.TextField(max_length=500)
    phonenumber=models.IntegerField()

    def __int__(self):
        return self.id


class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default="")
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

    def get_total(self):
        return self.quantity * self.product.price









class Orders(models.Model):
    PAYMENT_METHODS = (
        ('COD', 'Cash On Delivery'),
        ('ONLINE', 'Online Payment')
    )
    
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=5000)
    name = models.CharField(max_length=90)
    amount = models.IntegerField(default=0)
    email = models.CharField(max_length=111)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='COD')
    payment_status = models.CharField(max_length=20, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name


class OrderUpdate(models.Model):
    update_id = models.AutoField(primary_key=True)
    order_id = models.IntegerField(default="")
    update_desc = models.CharField(max_length=5000)
    delivered=models.BooleanField(default=False)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.update_desc[0:7] + "..."





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
