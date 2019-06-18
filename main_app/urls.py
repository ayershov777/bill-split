from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/signup', views.signup, name='signup'),
    path('groups/create/', views.GroupCreate.as_view(), name='group_create'),
    path('groups/<int:id>', views.group_detail, name='group_detail')
]
