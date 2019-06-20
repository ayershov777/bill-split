from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Group(models.Model):
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class Payment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.IntegerField()

    @classmethod
    def make_payment(cls, group, user, amount):
        user_payment = Payment.objects.all().get(group=group, holder=user)
        user_payment.amount += amount
        user_payment.save()

        group_payments = Payment.objects.all().filter(group=group)

        total = 0
        for payment in group_payments:
            if payment.amount > 0:
                total += payment.amount

        for payment in group_payments:
            if payment.amount > 0:
                ratio = payment.amount / total
                print(ratio)
                deposit = amount * ratio
                payment.amount -= deposit
                payment.save()
        

    @classmethod
    def __updatePayment(cls, group, user, amount):
        payment = Payment.objects.filter(group=group, holder=user)
        if (payment.count() == 0):
            payment = Payment(group=group, holder=user, amount=amount)
        else:
            payment = payment[0]
            payment.amount += amount
        payment.save()

    @classmethod
    def split_bill(cls, amount, group, users):
        holder = users[0]
        split_amount = amount / len(users)
        user_owed = amount - split_amount
        
        Payment.__updatePayment(group, holder, user_owed)
        for user in users[1:]:
            Payment.__updatePayment(group, user, -split_amount)
