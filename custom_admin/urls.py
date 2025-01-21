from django.urls import path
from . import views

app_name = 'custom_admin'

urlpatterns = [
    path('', views.dashboard_view, name='custom_admin_dashboard'),

    # Product Management
    path('products/', views.manage_products_view, name='manage_products'),
    path('products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('add-product/', views.add_product, name='add_product'),

    # Order Management
    path('orders/', views.manage_orders_view, name='manage_orders'),

    # User Management
    path('users/', views.list_users_view, name='manage_users'),         # List users
    path('users/create/', views.create_user_view, name='create_user'),  # Create user
    path('users/<int:user_id>/activate/', views.activate_user_view, name='activate_user'),
    path('users/<int:user_id>/deactivate/', views.deactivate_user_view, name='deactivate_user'),

    # Slider Management
    path('sliders/', views.slider_dashboard, name='slider_dashboard'),
    path('sliders/add/', views.add_slider, name='add_slider'),
    path('sliders/edit/<int:pk>/', views.edit_slider, name='edit_slider'),
    path('sliders/delete/<int:pk>/', views.delete_slider, name='delete_slider'),
]
