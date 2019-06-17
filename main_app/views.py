from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.views.generic.edit import CreateView

from .models import User
from .forms import SignupForm

def home(request):
    return render(request, 'home.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = SignupForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('/')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = SignupForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

# def signup(request):
#     model = User
#     signup_form = SignupForm()
#     return render(request, 'main_app/user_form.html', {
#         'signup_form': signup_form
#     })
