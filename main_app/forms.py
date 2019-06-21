from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import User, Group

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username']

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group
        fields = ['title']

class EditUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
