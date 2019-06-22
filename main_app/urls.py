from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('user/', views.edit_user, name='edit_user'),
    path('groups/', views.group_create, name='group_create'),
    path('groups/<int:id>', views.group_detail, name='group_detail'),
    path('groups/<int:id>/pay/', views.make_payment, name='make_payment'),
    path('groups/<int:id>/split/', views.split_bill, name='split_bill'),
    path('groups/<int:id>/users/', views.search_users, name='search_users'),
    path('notifications/', views.get_notifications, name='get_notifications')
]
