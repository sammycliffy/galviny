from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProfileForm, WalletForm
from django.http import HttpResponse
from app.models import Testimony, Plan
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from app.token import account_activation_token
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
import datetime
from datetime import timedelta
import pytz
from django.utils import timezone
from django.db.models import F, Count, Value
from background_task import background
import time
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import Celery
from celery.schedules import crontab



def index(request):
    return render(request, 'app/index.html')



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.email_confirmed = True
        user.save()
        login(request, user)
        return redirect('profile_completion')
    else:
        return render(request, 'account_activation_invalid.html')

def send_email(request):
    send_mail('Texting', 'Just want to be sure that this django thing is working', 'sammycliffy15@gmail.com', ['sammycliffy15@gmail.com',])
    return HttpResponse('Message sent')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('app/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            send_mail(subject, message, 'Galviny', [user.email])
            return HttpResponse('<h2>Check your email, activation link has been sent. click on the link to continue</h2>')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')    
    else:
        form = SignUpForm()
    return render(request, 'app/signup.html', {'form': form})

app = Celery()

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(10.0, test(), name='add every 10')

    # Calls test('world') every 30 seconds
    #sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    #sender.add_periodic_task(
     #   crontab(hour=7, minute=30, day_of_week=1),
   #     test.s('Happy Mondays!'),
    #)

@app.task
#def test():
     # Plan.objects.filter(plan__iexact='cryptocurrency',amount=50000, confirmed =True).update(profit =F('profit')+1200)

#test.s()


@periodic_task(run_every=(crontab(minute='*/3')), name="some_task", ignore_result=True)
def test():
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=50000, confirmed =True).update(profit =F('profit')+1200)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=100000, confirmed =True).update(profit =F('profit')+2400)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=200000, confirmed =True).update(profit =F('profit')+4800)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=300000, confirmed =True).update(profit =F('profit')+7200)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=400000, confirmed =True).update(profit =F('profit')+9600)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=500000, confirmed =True).update(profit =F('profit')+12000)
      Plan.objects.filter(plan__iexact='cryptocurrency',amount=100000, confirmed =True).update(profit =F('profit')+24000)
test()
@login_required
def profile(request):  
    username = request.user.username
    profit = Plan.objects.get(username=username)
    data = {
        'profit':profit.profit
    }

    return render(request, 'app/profile.html',data)


@login_required
def profile_completion(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            user = form.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'app/profile_completion.html',{'form':form})




@login_required
def fund_wallet(request):
    return render (request, 'app/fund_wallet.html')


@login_required
def cryptocurrency(request):
    if request.method == "POST":
        form = WalletForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse('saved successfully')
    else:
        form = WalletForm()
    return render(request, 'app/cryptocurrency.html', {'form':WalletForm})

#Withdrawal
@login_required
def withdrawal(request):
    return render(request, 'app/withdrawal.html')


def oil(request):
    return render(request, 'app/oil.html')

def testimony(request):
    if request.method == "POST":
        testimony = request.POST.get('testmony')
        username = request.user.username
        if testimony and username is not None:
            Testimony.objects.create(
                username = username,
                testimony = Testimony
            )
            return HttpResponse('Thank you for sharing your testimony with us')
    return render(request, 'app/testimony.html')


def forex(request):
    return render(request, 'app/forex.html')


@login_required
def update_profile(request):
    if request.method == 'POST':
        user_form = SignupForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            Profile_form.save()
            messages.success(request, _('Your profile was successfully updated!'))
            return redirect('settings:profile')
        else:
            messages.error(request, _('Please correct the error below.'))
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'app/editprofile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'app/change_password.html', {
        'form': form
    })