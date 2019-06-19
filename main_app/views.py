from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse
from .models import User, Group
from .forms import SignupForm, GroupCreateForm, AddUserForm

def home(request):
    if(request.user.is_authenticated):
        groups = User.objects.get(id=request.user.id).group_set.all()
        group_create_form = GroupCreateForm()
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

def group_create(request):
    title = request.POST.get("title", None)
    group = Group.objects.create(title=title)
    group.users.add(request.user)
    return redirect(f'/groups/{group.id}')


@login_required
def group_detail(request, id):
    if request.method == 'POST':
        usernames = request.POST.get("username", "")
        usernames = usernames.split('-')
        for username in usernames:
            userCount = User.objects.filter(username=username).count()
            if userCount:
                user = User.objects.get(username=username)
                group = Group.objects.get(id=id)
                group.users.add(user)
        return JsonResponse({'message' : 'ok'})

    group = Group.objects.get(id=id)
    username = request.user.username
    if group.users.filter(username=username):
        user_form = AddUserForm
        users = group.users.all()
        return render(request, 'groups/detail.html', {
            'user_form': user_form,
            'group': group,
            'users': users
        })
    else:
        return HttpResponse("You can't access this page")

def search_users(request, id):
    username = request.GET.get('username', "")
    usernames = []

    if username != "":
        users = list(User.objects.exclude(username__in=Group.objects.get(id=id).users.all().values_list('username')).filter(username__icontains=username))
        for user in users:
            usernames.append(user.username)

    return JsonResponse(usernames, safe=False)
