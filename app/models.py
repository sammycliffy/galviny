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
    sex = models.CharField(max_length=255, null=True)
    bank = models.CharField(max_length=255, null=True)
    account_name = models.CharField(max_length = 255, null=True)
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
    