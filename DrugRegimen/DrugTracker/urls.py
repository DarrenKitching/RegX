from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home', views.home, name='home'),
    path('dose/<doseURL>/', views.takeDose, name='takeDose'),
]