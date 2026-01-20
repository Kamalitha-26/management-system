from django.urls import path,include
from .views import home
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.visitor_registration, name='visitor_registration'),
]