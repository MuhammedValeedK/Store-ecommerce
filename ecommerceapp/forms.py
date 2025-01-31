from django import forms
from .models import Product, Slider, Category

# Form for the Product model
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically set the choices for the category field
        self.fields['category'].choices = [(category.id, category.name) for category in Category.objects.all()]


# Form for the Slider model
class SliderForm(forms.ModelForm):
    class Meta:
        model = Slider
        fields = ['title', 'subtitle', 'image', 'button_text', 'button_link', 'order']


# Form for the Category model
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'