from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Group, Payment, Split

admin.site.register(User, UserAdmin)
admin.site.register(Group)
admin.site.register(Payment)
admin.site.register(Split)