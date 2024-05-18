from django.urls import path
from . import views

app_name = "restaurant"

urlpatterns = [
    path('', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('menu/add/', views.add_menu_item, name='add_menu_item'),
    path('menu/<int:pk>/edit/', views.item_update, name='edit_menu_item'),
    path('menu/', views.menu, name='menu'),
   
]