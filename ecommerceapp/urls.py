from django.urls import path
from ecommerceapp import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
   
    path('', views.index , name="index"),
    path('contact', views.contact , name="contact"),
    path('about', views.about , name="about"),
    path('list/', views.product_list, name='product_list'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.view_cart, name='view_cart'),  # Cart page
    path('clear-cart/', views.clear_cart, name='clear_cart'),  # Clear cart
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('category/<slug:val>/', views.category_view.as_view(), name="category"),
    path('checkout/', views.checkout , name="checkout"),
    path('proceed-to-pay/', views.razorpaycheck ),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
