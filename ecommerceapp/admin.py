from django.contrib import admin
from ecommerceapp.models import  Contact,Product,Orders,OrderUpdate, Category
from .models import Slider


# Register your models here.

admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)


# Custom admin class for Product
from django.contrib import admin
from .models import Product, Category

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'category', 'subcategory', 'price', 'desc')
    search_fields = ('product_name', 'category', 'subcategory')
    list_filter = ('category', 'subcategory')
    ordering = ('price',)

    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'category':
            kwargs['choices'] = [(category.name, category.name) for category in Category.objects.all()]
        return super().formfield_for_choice_field(db_field, request, **kwargs)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Slider)
class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)





