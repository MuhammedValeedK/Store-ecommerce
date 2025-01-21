from django import forms
from .models import Product, Slider

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['product_name', 'price', 'category', 'subcategory', 'desc', 'image'] 



class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order']
