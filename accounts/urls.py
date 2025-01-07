from django.urls import path 
from accounts import views


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
     path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(),name='activate'),
]
