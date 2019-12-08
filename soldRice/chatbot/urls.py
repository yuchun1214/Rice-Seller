from django.urls import path

from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('testing/', views.testing, name='testing'),
    path('callback/',views.callback, name='callback'),
]
