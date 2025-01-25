from django import forms
from .models import Product, Slider

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__' 



class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order']
