from django.urls import path
from auth_app import views

urlpatterns = [
    path('register/', views.create_user_with_profile,
         name='create_user_with_profile'),
    path('login/', views.login_user, name='login_user'),
]
