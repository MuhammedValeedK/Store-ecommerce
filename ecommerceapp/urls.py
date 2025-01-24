from django.urls import path
from ecommerceapp import views

urlpatterns = [
   
    path('', views.index , name="index"),
    path('contact', views.contact , name="contact"),
    path('about', views.about , name="about"),
    path('category/<slug:val>/', views.category_view.as_view(), name="category"),
    path('checkout/', views.checkout , name="checkout"),
    path('proceed-to-pay/', views.razorpaycheck ),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    
]
