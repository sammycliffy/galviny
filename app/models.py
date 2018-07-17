from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile (models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    firstname = models.CharField(max_length=255, null=True, )
    lastname = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    age = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=255, null=True)
    sex = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    account_name = models.CharField(max_length = 255, null=True)
    occupation = models.CharField(max_length = 255, null=True)
    account_number = models.CharField(max_length = 255, null=True)
    email_confirmed = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Wallet(models.Model):
    user = models.CharField(max_length=255, null= True)
    email = models.EmailField(max_length=255, null = True)
    plan = models.CharField( max_length = 255, null = True)
    amount = models.CharField(max_length = 255, null= True)
    date = models.DateField(max_length=255, null = True)

class Testimony(models.Model):
    username = models.CharField(max_length = 255, null = True)
    testimony = models.CharField(max_length = 255, null = True)
    date = models.DateField(auto_now=True)
    confirmed = models.BooleanField(default=False)


class Cryptocurrency(models.Model):
    username = models.CharField(max_length = 255, null = True)
    choice = models.PositiveIntegerField( null = True)
    lent = models.CharField(max_length = 255, blank=True, )
    confirmed = models.BooleanField(default=False)
    profit = models.PositiveIntegerField(null=True, default=0)
    deposit_date = models.DateTimeField(auto_now=True)
    lend_date = models.DateTimeField(null=True, blank=True)
    amount_lent = models.PositiveIntegerField(null=True, default=0)
    previous_withdraw = models.PositiveIntegerField(null = True, default = 0)
    logistics = models.PositiveIntegerField(null = True, default = 0)

    def __str__(self):
        return self.username

class Forex(models.Model):
    username = models.CharField(max_length = 255, null = True)
    choice = models.PositiveIntegerField( null = True)
    lent = models.CharField(max_length = 255, blank=True, )
    confirmed = models.BooleanField(default=False)
    profit = models.PositiveIntegerField(null=True, default=0)
    deposit_date = models.DateTimeField(auto_now=True)
    lend_date = models.DateTimeField(null=True, blank=True)
    amount_lent = models.PositiveIntegerField(null=True, default=0)
    previous_withdraw = models.PositiveIntegerField(null = True, default = 0)
    def __str__(self):
        return self.username

class Oil(models.Model):
    username = models.CharField(max_length = 255, null = True)
    choice = models.PositiveIntegerField( null = True)
    lent = models.CharField(max_length = 255, blank=True, )
    confirmed = models.BooleanField(default=False)
    profit = models.PositiveIntegerField(null=True, default=0)
    deposit_date = models.DateTimeField(auto_now=True)
    lend_date = models.DateTimeField(null=True, blank=True)
    amount_lent = models.PositiveIntegerField(null=True, default=0)
    previous_withdraw = models.PositiveIntegerField(null = True, default = 0)
    def __str__(self):
        return self.username



class Withdraw(models.Model):
    username = models.CharField(max_length = 255, null = True)
    plan = models.CharField(max_length = 255, null = True)
    withdraw_amount = models.PositiveIntegerField(null = True)
    date = models.DateTimeField(null = True, blank=True)
    previous_withdraw = models.PositiveIntegerField(null = True, default = 0)
    logistics = models.PositiveIntegerField(null = True, default = 0)
    def __str__(self):
        return self.username




class Referrer(models.Model):
    referee = models.CharField(max_length = 255, null = True)
    referred = models.CharField(max_length = 255, null = True)
    amount = models.PositiveIntegerField(null = True )
    date = models.DateTimeField(auto_now=True)


class Newsletter(models.Model):
    email = models.EmailField(null = True)
    date = models.DateField(auto_now=True)