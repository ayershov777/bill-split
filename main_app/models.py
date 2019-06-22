from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Group(models.Model):
    title = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

class Notification(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    message = models.CharField(max_length=200)
    users = models.ManyToManyField(User)

    @classmethod
    def send_notifications(cls, code, sender_id, group, users, **kwargs):
        spent_on = kwargs.get('spent_on', None)
        amount = kwargs.get('amount', None)

        sender = User.objects.get(id=sender_id)

        sender_name = sender.first_name
        group_name = group.title

        if code == 0:
            message = f"{sender_name} invited you to group {group_name}"
        elif code == 1:
            message = f"{sender_name} split a payment with you for {spent_on}, in group {group_name}"
        elif code == 2:
            message = f"{sender_name} paid {amount} to group {group_name}"
        else:
            message = "error!"

        notification = Notification(group=group, message=message)
        notification.save()
        notification.users.set(users)
    
class Payment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

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

class Split(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    payer = models.ForeignKey(User, on_delete=models.CASCADE)
    users = models.CharField(max_length=9999)
    amount = models.DecimalField(max_digits=12, decimal_places=2) #amount B owes to A
    date = models.DateField()
    spent_on = models.CharField(max_length=20)