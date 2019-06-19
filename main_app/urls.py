from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('groups/', views.group_create, name='group_create'),
    path('groups/<int:id>', views.group_detail, name='group_detail'),
    path('groups/<int:id>/users/', views.search_users, name='search_users')
]
