from django.contrib import admin
from ecommerceapp.models import  Contact,Product,Orders,OrderUpdate
from .models import Slider


# Register your models here.

admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)


# Custom admin class for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'subcategory', 'price', 'desc')  # Columns to display in admin list view
    search_fields = ('product_name', 'category', 'subcategory')  # Add a search bar
    list_filter = ('category', 'subcategory')  # Add filter options
    ordering = ('price',)  # Default ordering

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
