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
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('search/', views.search_products, name='search_products'),
    path('checkout/', views.checkout , name="checkout"),
    path('checkout/success/', views.checkout_success, name='checkout_success'),
    path('checkout/cancel/', views.checkout_cancel, name='checkout_cancel'),
    path('create-stripe-session/', views.create_stripe_session, name='create_stripe_session'),
    path('order-summary/', views.order_summary, name='order_summary'),

    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('wishlist/remove/<int:product_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('wishlist/', views.view_wishlist, name='view_wishlist'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
