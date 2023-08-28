from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/<str:username>', views.About.as_view(), name='about'),
    path('register/', views.UserRegisterView.as_view(), name='user_register'),
    path('writer/', views.WriterView.as_view(), name='writers')
]