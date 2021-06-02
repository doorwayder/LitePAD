from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.neworder),
    path('neworder/', views.neworder, name='neworder'),
    path('orders/', views.orders, name='orders'),
    path('stat/', views.statorders, name='stat'),
]
