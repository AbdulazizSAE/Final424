from django.urls import path
from . import views
from django.views.generic.base import RedirectView

app_name = 'restaurant'

urlpatterns = [
    path('', RedirectView.as_view(url='login/', permanent=False), name='home'),
    path('menu/', views.menu, name='menu'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('add/', views.add_menu_item, name='add_menu_item'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/<int:pk>/edit/', views.item_update, name='edit_menu_item'),
]
