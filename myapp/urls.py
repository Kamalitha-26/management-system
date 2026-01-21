from django.urls import path,include
from .views import home
from . import views
from .views import dashboard

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.visitor_registration, name='visitor_registration'),
    path('dasboard/', views.dashboard, name='dashboard'),
]