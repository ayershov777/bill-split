from django.shortcuts import render, redirect

from django.contrib.auth import login
from django.views.generic.edit import CreateView

from .models import User, Group
from .forms import SignupForm, GroupCreateForm

def home(request):
    if(request.user.is_authenticated):
        groups = User.objects.get(id=request.user.id).group_set.all()
        group_create_form = GroupCreateForm()
        print(len(groups))
        return render(request, 'users/detail.html', {
            'groups': groups,
            'group_create_form': group_create_form
        })
    else:
        return render(request, 'home.html')
    

def signup(request):

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
            return render(request, 'registration/signup.html', {
                'form': form
            })
    # A bad POST or a GET request, so render signup.html with an empty form
    form = SignupForm()
    context = {'form': form}
    return render(request, 'registration/signup.html', context)

class GroupCreate(CreateView):
    model = Group
    fields = ['title', 'users']
    success_url = '/'