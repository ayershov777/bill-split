from django.core import serializers
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.http import HttpResponse, JsonResponse
from .models import User, Group, Payment, Split, Notification
from .forms import SignupForm, GroupCreateForm, EditUserForm
from decimal import *
from datetime import date

def home(request):
    if(request.user.is_authenticated):
        groups = User.objects.get(id=request.user.id).group_set.all()
        group_create_form = GroupCreateForm()
        edit_user_form = EditUserForm()
        return render(request, 'users/detail.html', {
            'groups': groups,
            'group_create_form': group_create_form,
            'edit_user_form': edit_user_form
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

def edit_user(request):
    form = EditUserForm(request.POST)
    if form.is_valid():
        user = request.user
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
    return redirect('/')

def group_create(request):
    title = request.POST.get("title", None)
    group = Group.objects.create(title=title)
    group.users.add(request.user)
    return redirect('/')

@login_required
def group_detail(request, id):
    if request.method == 'POST':
        usernames = request.POST.get("username", "")
        usernames = usernames.split('-')
        user_ids = []
        for username in usernames:
            userCount = User.objects.filter(username=username).count()
            if userCount:
                user = User.objects.get(username=username)
                user_ids.append(user.id)
                group = Group.objects.get(id=id)
                group.users.add(user)
        Notification.send_notifications(0, request.user.id, group, User.objects.filter(id__in=user_ids))        
        return JsonResponse({'message' : 'ok'})

    group = Group.objects.get(id=id)
    username = request.user.username
    if group.users.filter(username=username):
        users = group.users.all()
        payment = Payment.objects.filter(group=group, holder=request.user)
        if len(payment) == 0:
            amount = 0
        else:
            amount = Decimal(payment[0].amount)

        if amount > 0:
            standing = "positive"
        elif amount < 0:
            standing = "negative"
            amount = -amount
        else:
            standing = "balanced"

        return render(request, 'groups/detail.html', {
            'group': group,
            'users': users,
            'amount': amount,
            'standing': standing,
            'splits': Split.objects.filter(group=group)
        })
    else:
        return HttpResponse("You can't access this page")

def make_payment(request, id):
    group = Group.objects.get(id=id)
    amount = Decimal(request.POST.get('amount', 0))
    Payment.make_payment(group, request.user, amount)
    Notification.send_notifications(2, request.user.id, group, group.users.exclude(id=request.user.id), amount=amount)
    return HttpResponse('ok')

def split_bill(request, id):
    group = Group.objects.get(id=id)
    usernames = request.POST.get('usernames', '')
    amount = Decimal(request.POST.get('amount', 0))
    spent_on = request.POST.get('spent_on', '')
    split = Split(group=group, payer=request.user, users=usernames, amount=amount, spent_on=spent_on, date=date.today())
    split.save()

    users = []
    for username in usernames.split('-'):
        user = User.objects.get(username=username)
        users.append(user)

    Payment.split_bill(amount, group, users)
    Notification.send_notifications(1, request.user.id, group, group.users.exclude(id=request.user.id), spent_on=spent_on)

    return HttpResponse('ok')

def search_users(request, id):
    username = request.GET.get('username', "")
    usernames = []

    if username != "":
        users = list(User.objects.exclude(username__in=Group.objects.get(id=id).users.all().values_list('username')).filter(username__icontains=username))
        for user in users:
            usernames.append(user.username)

    return JsonResponse(usernames, safe=False)

def get_notifications(request):
    notifications = request.user.notification_set.all()
    return JsonResponse(notifications, safe=False)