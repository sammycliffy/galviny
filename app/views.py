from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProfileForm, WalletForm
from django.http import HttpResponse
from app.models import Testimony, Cryptocurrency, Forex, Oil
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
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse




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






@login_required
def cryptocurrency(request):
    if request.method == "POST":
        username = request.user.username
        choice = request.POST.get('choice')
        Cryptocurrency.objects.create(
            username = username,
            choice = choice,
        )
        
    return render(request, 'app/cryptocurrency.html', {'form':WalletForm})




def lendmoney(request):
    if request.method == 'POST':
        try:
            check = Cryptocurrency.objects.get(username = request.user.username)
            if check.lent != 'True':
                Cryptocurrency.objects.filter( username=request.user.username,  confirmed= True).update(
                    lent = 'True',
                    lend_date = datetime.datetime.now()
                )
        except ObjectDoesNotExist:
            try:
                check = Forex.objects.get(username = request.user.username)
                if check.lent != 'True':
                    Forex.objects.filter( username=request.user.username,  confirmed= True).update(
                        lent = 'True',
                        lend_date = datetime.datetime.now()
                    )
            except ObjectDoesNotExist:
                try:
                    check = Oil.objects.get(username = request.user.username)
                    if check.lent != 'True':
                        Oil.objects.filter( username=request.user.username,  confirmed= True).update(
                            lent = 'True',
                            lend_date = datetime.datetime.now()
                        )
                except ObjectDoesNotExist:
                    data = {
                        'balance':0
                    }
                    if data['balance']:
                        data['error_message'] = 'You have no money'
                        return JsonResponse(data)
       
    return render(request, 'app/profile.html')
      


@login_required
def profile(request): 
     try:
        profile = Cryptocurrency.objects.get( username=request.user.username,  lent= True)
        paid_date = profile.lend_date    
        choice = profile.choice
        end_date = paid_date + timedelta(days=60)
        current_day = timezone.now()
        profit_days = current_day - paid_date
        profit_days = profit_days.days
        if choice == 50000 and paid_date <= end_date:
            profit = 1200 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                        
                    } 
        elif choice == 100000 and paid_date <= end_date:
            profit = 2400 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        elif choice == 200000 and paid_date <= end_date:
            profit = 4800 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        elif choice == 300000 and paid_date <= end_date:
            profit = 7200 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        elif choice == 400000 and paid_date <= end_date:
            profit = 9600 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        elif choice == 500000 and paid_date <= end_date:
            profit = 12000 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        elif choice == 1000000 and paid_date <= end_date:
            profit = 24000 * profit_days
            data = {
                        'profit':profit,
                        'wallet_balance':profile.choice,
                        'date':paid_date
                    } 
        return render(request, 'app/profile.html', data)
     except ObjectDoesNotExist:
         #Forex
            try:
                profile = Forex.objects.get( username=request.user.username,  lent= True)
                paid_date = paid_date  
                choice = profile.choice
                end_date = paid_date + timedelta(days=60)
                current_day = timezone.now()
                profit_days = current_day - paid_date
                profit_days = profit_days.days
                if choice == 100000 and paid_date <= end_date:
                    profit = 1700 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
                elif choice == 200000 and paid_date <= end_date:
                    profit = 3400 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
                elif choice == 300000 and paid_date <= end_date:
                    profit = 5100 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
                elif choice == 400000 and paid_date <= end_date:
                    profit = 6800 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
                elif choice == 500000 and paid_date <= end_date:
                    profit = 8500 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
                elif choice == 600000 and paid_date <= end_date:
                    profit = 10200 * profit_days
                    data = {
                                'profit':profit,
                                'wallet_balance':profile.choice,
                                'date':paid_date
                            } 
            except ObjectDoesNotExist:
            #Oil and gas
                try:
                    profile = Oil.objects.get( username=request.user.username,  lent= True)
                    paid_date = paid_date  
                    choice = profile.choice
                    end_date = paid_date + timedelta(days=60)
                    current_day = timezone.now()
                    profit_days = current_day - paid_date
                    profit_days = profit_days.days
                    if choice == 40000 and paid_date <= end_date:
                        profit = 900 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 60000 and paid_date <= end_date:
                        profit = 1350 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 80000 and paid_date <= end_date:
                        profit = 1800 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 100000 and paid_date <= end_date:
                        profit = 2250 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 200000 and paid_date <= end_date:
                        profit = 4500 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 300000 and paid_date <= end_date:
                        profit = 6750 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                    elif choice == 400000 and paid_date <= end_date:
                        profit = 9000 * profit_days
                        data = {
                                    'profit':profit,
                                    'wallet_balance':profile.choice,
                                    'date':paid_date
                                } 
                except ObjectDoesNotExist:
                    profit = 0

                    data = {
                                    'profit':profit,
                                    'wallet_balance':0,
                                    'date':'No money lent'
                            } 

                    return render(request, 'app/profile.html', data)
     
     return render(request, 'app/profile.html')

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



#Withdrawal
@login_required
def withdrawal(request):
    return render(request, 'app/withdrawal.html')


def oil(request):
    if request.method == "POST":
        username = request.user.username
        choice = request.POST.get('choice')
        Oil.objects.create(
            username = username,
            choice = choice,
        )
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


@login_required
def forex(request):
    if request.method == "POST":
        username = request.user.username
        choice = request.POST.get('choice')
        Forex.objects.create(
            username = username,
            choice = choice,
        )
        
    return render(request, 'app/forex.html', {'form':WalletForm})



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