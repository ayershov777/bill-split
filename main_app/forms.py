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
<<<<<<< HEAD
        fields = ['title', 'users']
=======
        fields = ['title']

class AddUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username']
>>>>>>> 7a88debd7847b344d39e6e8d7be8996c6d936468
