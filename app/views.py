from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, ProfileForm, WalletForm
from django.http import HttpResponse
from app.models import Testimony, Cryptocurrency, Forex, Oil, Withdraw, Referrer, Newsletter, Expired_Referrer, Payable_referral, Deleted, Referral_Payment 
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
from django.db.models import Sum




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
        referrer_link = request.POST.get('referrer')
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            user.is_active = False
            user.save()
            #username = self.cleaned_data.get('email')
            current_site = get_current_site(request)
            subject = 'Activate Your MySite Account'
            message = render_to_string('app/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })
            referrer_link = referrer_link.split('=')[-1]
            check_start = referrer_link.startswith('/')
            print(check_start)
            if check_start == True:
                print('yes')
            else:
                print ('no')
            exists =  Referrer.objects.filter(referred__iexact=user.username).exists()
            if check_start != True and exists != True:
                Referrer.objects.create(
                    referee = referrer_link,
                    referred = user.username
                )
                Referral_Payment.objects.create(
                    username = form.cleaned_data['username'],
                    previous_username = referrer_link
                )
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
        real_choice = choice[0:-2]
        data = {
            'already_done': Cryptocurrency.objects.filter(username__iexact=username).exists(),
        }
        if data['already_done']:
            data['error_message'] = 'sorry you cannot do more than once'
            return JsonResponse(data)
        else:
            Cryptocurrency.objects.create(
                username = username,
                choice = real_choice,
            )
        
    return render(request, 'app/cryptocurrency.html', {'form':WalletForm})




def lendmoney(request):
    if request.method == 'POST':
        try:
            check = Cryptocurrency.objects.get(username = request.user.username)
            if check.lent != 'True':
                amount_lent = check.choice
                Cryptocurrency.objects.filter( username=request.user.username,  confirmed= True).update(
                    lent = 'True',
                    lend_date = datetime.datetime.now(),
                    amount_lent = amount_lent,
                    choice = 0
                    
                )
        except ObjectDoesNotExist:
            try:
                check = Forex.objects.get(username = request.user.username)
                if check.lent != 'True':
                    amount_lent = check.choice
                    Forex.objects.filter( username=request.user.username,  confirmed= True).update(
                        lent = 'True',
                        lend_date = datetime.datetime.now(),
                        amount_lent = amount_lent,
                        choice = 0
                    )
            except ObjectDoesNotExist:
                try:
                    check = Oil.objects.get(username = request.user.username)
                    if check.lent != 'True':
                        amount_lent = check.choice
                        Oil.objects.filter( username=request.user.username,  confirmed= True).update(
                            lent = 'True',
                            lend_date = datetime.datetime.now(),
                            amount_lent = amount_lent,
                            choice = 0
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
        profile = Cryptocurrency.objects.get(username = request.user.username)
        if profile.lent == 'True':
            paid_date = profile.lend_date    
            choice = profile.choice
            end_date = paid_date + timedelta(days=5)
            current_day = timezone.now()
            profit_days = current_day - paid_date
            profit_days = profit_days.days
            before_ten_days = profile.lend_date + timedelta(days=10)
            if current_day < end_date:
                    if profile.amount_lent == 50000:
                        profit = 1200 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 100000:
                        profit = 2400 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 200000 and paid_date:
                        profit = 4800 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 300000 and paid_date:
                        profit = 7200 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 400000 and paid_date:
                        profit = 9600 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 500000 and paid_date:
                        profit = 12000 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
                    elif profile.amount_lent == 1000000 and paid_date:
                        profit = 24000 * profit_days - profile.previous_withdraw - profile.logistics
                        Cryptocurrency.objects.filter(username = request.user.username).update(
                            profit = profit
                        )
                        profile = Cryptocurrency.objects.get(username = request.user.username)
                        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':paid_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
                        return render(request, 'app/profile.html', data)
            else:
                try:
                    delete = Cryptocurrency.objects.get(username = request.user.username)
                    try:
                        new_p = Deleted.objects.get(username=request.user.username)
                        data = {
                                            'profit':new_p.profit,    
                                        } 
                        Cryptocurrency.objects.get(username=request.user.username).delete()
                        return render(request, 'app/profile.html', data)
                    except ObjectDoesNotExist:
                        deleted = Deleted.objects.create(username=request.user.username, profit=delete.profit)
                        new_p = Deleted.objects.get(username=request.user.username)
                        data = {
                                            'profit':new_p.profit,    
                                        } 
                        Cryptocurrency.objects.get(username=request.user.username).delete()
                        return render(request, 'app/profile.html', data)
                except ObjectDoesNotExist:
                    try:
                        delete = Forex.objects.get(username = request.user.username)
                        try:
                            new_p = Deleted.objects.get(username=request.user.username)
                            data = {
                                                'profit':new_p.profit,    
                                            } 
                            Forex.objects.get(username=request.user.username).delete()
                            return render(request, 'app/profile.html', data)
                        except ObjectDoesNotExist:
                            deleted = Deleted.objects.create(username=request.user.username, profit=delete.profit)
                            new_p = Deleted.objects.get(username=request.user.username)
                            data = {
                                                'profit':new_p.profit,    
                                            } 
                            Forex.objects.get(username=request.user.username).delete()
                            return render(request, 'app/profile.html', data)
                    except ObjectDoesNotExist:
                            delete = Oil.objects.get(username = request.user.username)
                            try:
                                new_p = Deleted.objects.get(username=request.user.username)
                                data = {
                                                    'profit':new_p.profit,    
                                                } 
                                Oil.objects.get(username=request.user.username).delete()
                                return render(request, 'app/profile.html', data)
                            except ObjectDoesNotExist:
                                deleted = Deleted.objects.create(username=request.user.username, profit=delete.profit)
                                new_p = Deleted.objects.get(username=request.user.username)
                                data = {
                                                    'profit':new_p.profit,    
                                                } 
                                Oil.objects.get(username=request.user.username).delete()
                                return render(request, 'app/profile.html', data)
                    
        else:
            try:
                    profile = Cryptocurrency.objects.get(username = request.user.username, confirmed=True)
                    data = {
                            'wallet_balance':profile.choice,
                            'amount':0.00,
                            'date':'No money lent',
                            'profit':0.00
                        }
                    return render(request, 'app/profile.html',data)
            except ObjectDoesNotExist:
                try:
                    profile = Forex.objects.get(username = request.user.username, confirmed=True)
                    data = {
                            'wallet_balance':profile.choice,
                            'amount':0.00,
                            'date':'No money lent',
                            'profit':0.00
                        }
                    return render(request, 'app/profile.html',data)
                except ObjectDoesNotExist:
                    try:
                        profile = Oil.objects.get(username = request.user.username, confirmed=True)
                        data = {
                                'wallet_balance':profile.choice,
                                'amount':0.00,
                                'date':'No money lent',
                                'profit':0.00
                            }
                        return render(request, 'app/profile.html',data)
                    except ObjectDoesNotExist:
                        pass


           
    except ObjectDoesNotExist:
        try:
            profile = Forex.objects.get(username = request.user.username)
            if profile.lent == 'True':
                paid_date = profile.lend_date    
                choice = profile.choice
                end_date = paid_date + timedelta(days=5)
                current_day = timezone.now()
                profit_days = current_day - paid_date
                profit_days = profit_days.days
                before_ten_days = profile.lend_date + timedelta(days=10)
                if current_day < end_date:
                        if profile.amount_lent == 100000:
                            profit = 1700 * profit_days - profile.previous_withdraw - profile.logistics
                            Forex.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                        } 
                            return render(request, 'app/profile.html', data)
                        elif profile.amount_lent == 200000:
                            profit = 3400 * profit_days - profile.previous_withdraw - profile.logistics
                            if profit <=0:
                                profit = 0
                            Forex.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                            
                                        } 
                            
                            return render(request, 'app/profile.html', data)
                        elif profile.amount_lent == 300000 and paid_date:
                            profile = Cryptocurrency.objects.get(username = request.user.username)
                            profit = 5100 * profit_days - profile.previous_withdraw - profile.logistics
                            if profit <=0:
                                profit = 0
                            Forex.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                            
                                        } 
                            
                            return render(request, 'app/profile.html', data)
                        elif profile.amount_lent == 400000 and paid_date:
                            profit = 6800 * profit_days - profile.logistics
                            if profit <=0:
                                profit = 0
                            Cryptocurrency.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                            
                                        } 
                            
                            return render(request, 'app/profile.html', data)
                        elif profile.amount_lent == 500000 and paid_date:
                            profit = 8500 * profit_days - profile.logistics
                            if profit <=0:
                                profit = 0
                            Forex.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                            
                                        } 

                            
                            return render(request, 'app/profile.html', data)
                        elif profile.amount_lent == 600000 and paid_date:
                            profit = 10200 * profit_days - profile.logistics
                            if profit <=0:
                                profit = 0
                            
                            Forex.objects.filter(username = request.user.username).update(
                                profit = profit
                            )
                            profile = Forex.objects.get(username = request.user.username)
                            data = {
                                        
                                            'wallet_balance':profile.choice,
                                            'date':paid_date,
                                            'profit':profile.profit,
                                            'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                            
                                        } 
                            
                            return render(request, 'app/profile.html', data)
        except ObjectDoesNotExist:

            try:
                profile = Oil.objects.get(username = request.user.username)
                if profile.lent == 'True':
                    paid_date = profile.lend_date    
                    choice = profile.choice
                    end_date = paid_date + timedelta(days=5)
                    current_day = timezone.now()
                    profit_days = current_day - paid_date
                    profit_days = profit_days.days
                    before_ten_days = profile.lend_date + timedelta(days=10)
                    if current_day < end_date:
                            if profile.amount_lent == 20000:
                                profit = 450 * profit_days - profile.previous_withdraw - profile.logistics
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                            } 
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 40000:
                                profit = 900 * profit_days - profile.previous_withdraw - profile.logistics
                                if profit <=0:
                                    profit = 0
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 
                                
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 60000 and paid_date:
                                profile = Oil.objects.get(username = request.user.username)
                                profit = 1350 * profit_days - profile.previous_withdraw - profile.logistics
                                if profit <=0:
                                    profit = 0
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 

                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 80000 and paid_date:
                                profit = 1800 * profit_days - profile.logistics
                                if profit <=0:
                                    profit = 0
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 
                                
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 100000 and paid_date:
                                profit = 2,250 * profit_days - profile.logistics
                                if profit <=0:
                                    profit = 0
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                            'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 

                                
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 200000 and paid_date:
                                profit = 4500 * profit_days - profile.logistics
                                if profit <=0:
                                    profit = 0
                                
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 
                                
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 300000 and paid_date:
                                profit = 6750 * profit_days - profile.logistics
                                if profit <=0:
                                    profit = 0
                                
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 
                                
                                return render(request, 'app/profile.html', data)
                            elif profile.amount_lent == 400000 and paid_date:
                                profit = 9000 * profit_days - profile.logistics
                                if profit <=0:
                                    profit = 0
                                
                                Oil.objects.filter(username = request.user.username).update(
                                    profit = profit
                                )
                                profile = Oil.objects.get(username = request.user.username)
                                data = {
                                            
                                                'wallet_balance':profile.choice,
                                                'date':paid_date,
                                                'profit':profile.profit,
                                                'amount':profile.amount_lent,
                                                'withdrawal':profile.previous_withdraw + profile.logistics
                                                
                                            } 
                                
                                return render(request, 'app/profile.html', data)
            except ObjectDoesNotExist:
                try:
                    if  Deleted.objects.get(username = request.user.username):
                        new_p = Deleted.objects.get(username=request.user.username)
                        data = {
                                                    'profit':new_p.profit,    
                                                } 
                                    
                        return render(request, 'app/profile.html', data)
                except ObjectDoesNotExist:
                    pass
    data = {
            
                    'amount':0.00,
                    'date':'No money lent',
                    'profit':0.00
                }
    return render(request, 'app/profile.html', data)



def referrer (request):

            total_referred = Referrer.objects.filter(referee = request.user.username)
            persons_referred = Referrer.objects.filter(referee = request.user.username).count()
            list_of_usernames = []
            for referred in total_referred:
                check_crypto = Cryptocurrency.objects.filter(username = referred.referred)     
                for i in check_crypto:
                    referred_amount = i.amount_lent * 0.03
                    print(referred_amount)
                    check_number = Referral_Payment.objects.filter(previous_username = referred.referred).count()
                    print (check_number)
                    if check_number <= 1:
                        referrer_amount = Referral_Payment.objects.filter(previous_username = request.user.username).update(amount= referred_amount)
                        referrer_amount = Referral_Payment.objects.filter(previous_username=request.user.username)
                        aggregation = referrer_amount.aggregate(amount=Sum('amount'))
                        result = aggregation.get('amount', 0)

                        data = {
                            'referrer_amount' : result,
                            'persons':persons_referred
                        }
                
                        return render(request, 'app/referral.html', data)
            return render(request, 'app/referral.html')
   


def profile_completion(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm()
    return render(request, 'app/profile_completion.html',{'form':form})




@login_required
def fund_wallet(request):
    return render (request, 'app/fund_wallet.html')

def withdrawal_failed(request):
    return render (request, 'app/withdrawal-failed.html')

def withdrawal_success(request):
    try:
        payment = Cryptocurrency.objects.get(username = request.user.username, lent=True)        
        expiry_date = payment.lend_date + timedelta(days = 5)
        before_ten_days = payment.lend_date + timedelta(days=10)
        current_date = timezone.now()
        logistics = 200
        if current_date <= before_ten_days:
                logistics = 2000
        withdraw_amount = payment.profit - payment.previous_withdraw -  logistics   
        if withdraw_amount <= 1000:
                return redirect('withdrawal_failed')
        else:
             
                if  Withdraw.objects.filter(username = request.user.username):
                    Withdraw.objects.filter(username = request.user.username).update(
                        username = request.user.username,
                        withdraw_amount = withdraw_amount,
                        plan = 'cryptocurrency',
                        date = datetime.datetime.now(),
                        previous_withdraw = F('previous_withdraw') + withdraw_amount,
                        logistics = logistics
                        )
                   
                    Referrer.objects.filter(referee = request.user.username).delete()
                    message = '{} made a withdrawal of {} with account number {} and bank {}'
                    subject = 'Withdrawal'
                    real_amount = withdraw_amount - logistics
                    sending = message.format(request.user.username,real_amount, request.user.profile.account_number, request.user.profile.bank)
                    send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                    Cryptocurrency.objects.filter(username = request.user.username).update(
                            previous_withdraw = F('previous_withdraw') + withdraw_amount,
                            logistics = logistics,
                            profit = 0
                        )
                    return render (request, 'app/withdrawal-success.html') 
                else:
                    Withdraw.objects.create(
                        username = request.user.username,
                        withdraw_amount = withdraw_amount,
                        plan = 'cryptocurrency',
                        previous_withdraw = withdraw_amount,
                        date = datetime.datetime.now(),
                        logistics =  logistics
                    )
                    message = '{} {} made a withdrawal of {} with account number {} and bank {}'
                    subject = 'Withdrawal'
                    sending = message.format(request.user.profile.firstname, request.user.profile.lastname, withdraw_amount, request.user.profile.account_number, request.user.profile.bank)
                    send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                    Referrer.objects.filter(referee = request.user.username).delete()
                    Cryptocurrency.objects.filter(username = request.user.username).update(
                        previous_withdraw = F('previous_withdraw') + withdraw_amount,
                        logistics =  logistics,
                        profit = 0
                        )
                    return render (request, 'app/withdrawal-success.html') 
                       
    except ObjectDoesNotExist:
        try:
            payment = Forex.objects.get(username = request.user.username, lent=True)        
            expiry_date = payment.lend_date + timedelta(days = 5)
            before_ten_days = payment.lend_date + timedelta(days=10)
            current_date = timezone.now()
            logistics = 200
            if current_date <= before_ten_days:
                    logistics = 2000
            withdraw_amount = payment.profit - payment.previous_withdraw -  logistics   
            if withdraw_amount <= 1000:
                    return redirect('withdrawal_failed')
            else:
                
                    if  Withdraw.objects.filter(username = request.user.username):
                        Withdraw.objects.filter(username = request.user.username).update(
                            username = request.user.username,
                            withdraw_amount = withdraw_amount,
                            plan = 'Forex',
                            date = datetime.datetime.now(),
                            previous_withdraw = F('previous_withdraw') + withdraw_amount,
                            logistics = logistics
                            )
                        Forex.objects.filter(username = request.user.username).update(
                                previous_withdraw = F('previous_withdraw') + withdraw_amount,
                                logistics = logistics,
                                profit = 0
                            )
                        Referrer.objects.filter(referee = request.user.username).delete()
                        message = '{} made a withdrawal of {} with account number {} and bank {}'
                        subject = 'Withdrawal'
                        real_amount = withdraw_amount - logistics
                        sending = message.format(request.user.username,real_amount, request.user.profile.account_number, request.user.profile.bank)
                        send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                        return render (request, 'app/withdrawal-success.html') 
                    else:
                        Withdraw.objects.create(
                            username = request.user.username,
                            withdraw_amount = withdraw_amount,
                            plan = 'Forex',
                            previous_withdraw = withdraw_amount,
                            date = datetime.datetime.now(),
                            logistics =  logistics
                        )
                        Forex.objects.filter(username = request.user.username).update(
                            previous_withdraw = F('previous_withdraw') + withdraw_amount,
                            logistics =  logistics,
                            profit = 0
                            )
                        message = '{} {} made a withdrawal of {} with account number {} and bank {}'
                        subject = 'Withdrawal'
                        sending = message.format(request.user.profile.firstname, request.user.profile.lastname, withdraw_amount, request.user.profile.account_number, request.user.profile.bank)
                        send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                        Referrer.objects.filter(referee = request.user.username).delete()
                        return render (request, 'app/withdrawal-success.html') 
        except ObjectDoesNotExist:
            try:
                payment = Oil.objects.get(username = request.user.username, lent=True)        
                expiry_date = payment.lend_date + timedelta(days = 5)
                before_ten_days = payment.lend_date + timedelta(days=10)
                current_date = timezone.now()
                logistics = 200
                if current_date <= before_ten_days:
                        logistics = 2000
                withdraw_amount = payment.profit - payment.previous_withdraw -  logistics   
                if withdraw_amount <= 1000:
                        return redirect('withdrawal_failed')
                else:
                    
                        if  Withdraw.objects.filter(username = request.user.username):
                            Withdraw.objects.filter(username = request.user.username).update(
                                username = request.user.username,
                                withdraw_amount = withdraw_amount,
                                plan = 'Oil',
                                date = datetime.datetime.now(),
                                previous_withdraw = F('previous_withdraw') + withdraw_amount,
                                logistics = logistics
                                )
                            Oil.objects.filter(username = request.user.username).update(
                                    previous_withdraw = F('previous_withdraw') + withdraw_amount,
                                    logistics = logistics,
                                    profit = 0
                                )
                            Referrer.objects.filter(referee = request.user.username).delete()
                            message = '{} made a withdrawal of {} with account number {} and bank {}'
                            subject = 'Withdrawal'
                            real_amount = withdraw_amount - logistics
                            sending = message.format(request.user.username,real_amount, request.user.profile.account_number, request.user.profile.bank)
                            send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                            return render (request, 'app/withdrawal-success.html') 
                        else:
                            Withdraw.objects.create(
                                username = request.user.username,
                                withdraw_amount = withdraw_amount,
                                plan = 'Oil',
                                previous_withdraw = withdraw_amount,
                                date = datetime.datetime.now(),
                                logistics =  logistics
                            )
                            Oil.objects.filter(username = request.user.username).update(
                                previous_withdraw = F('previous_withdraw') + withdraw_amount,
                                logistics =  logistics,
                                profit = 0
                                )
                            message = '{} {} made a withdrawal of {} with account number {} and bank {}'
                            subject = 'Withdrawal'
                            sending = message.format(request.user.profile.firstname, request.user.profile.lastname, withdraw_amount, request.user.profile.account_number, request.user.profile.bank)
                            send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                            Referrer.objects.filter(referee = request.user.username).delete()
                            return render (request, 'app/withdrawal-success.html') 
            except ObjectDoesNotExist:
                if Deleted.objects.get(username=request.user.username):
                    new_p = Deleted.objects.get(username=request.user.username)
                    if  Withdraw.objects.filter(username = request.user.username):
                            Withdraw.objects.filter(username = request.user.username).update(
                                username = request.user.username,
                                withdraw_amount = new_p.profit - 2000,
                                plan = 'cryptocurrency',
                                date = datetime.datetime.now(),
                                previous_withdraw = F('previous_withdraw') + new_p.profit,
                                logistics = 2000
                                )
                            
                            Referrer.objects.filter(referee = request.user.username).delete()
                            message = '{} made a withdrawal of {} with account number {} and bank {}'
                            subject = 'Withdrawal'
                            real_amount = new_p.profit - 2000
                            sending = message.format(request.user.username,real_amount, request.user.profile.account_number, request.user.profile.bank)
                            send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                            Deleted.objects.get(username=request.user.username).delete()
                            return render (request, 'app/withdrawal-success.html') 
                    else:
                            Withdraw.objects.create(
                                username = request.user.username,
                                withdraw_amount = new_p.profit - 2000,
                                plan = 'cryptocurrency',
                                previous_withdraw = new_p.profit - 2000,
                                date = datetime.datetime.now(),
                                logistics =  2000
                            )
                            message = '{} {} made a withdrawal of {} with account number {} and bank {}'
                            subject = 'Withdrawal'
                            sending = message.format(request.user.profile.firstname, request.user.profile.lastname, withdraw_amount, request.user.profile.account_number, request.user.profile.bank)
                            send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
                            Referrer.objects.filter(referee = request.user.username).delete()
                            Deleted.objects.get(username=request.user.username).delete()
                            return render (request, 'app/withdrawal-success.html') 
                
#Withdrawal
@login_required
def withdrawal(request):
    try:
        profile = Cryptocurrency.objects.get(username = request.user.username)
        data = {
                                    
                                        'wallet_balance':profile.choice,
                                        'date':profile.lend_date,
                                        'profit':profile.profit,
                                        'amount':profile.amount_lent,
                                        'withdrawal':profile.previous_withdraw + profile.logistics
                                        
                                    } 
        return render(request, 'app/withdrawal.html',data)
    except ObjectDoesNotExist:
        try:
                new_p = Deleted.objects.get(username=request.user.username)
                data = {
                                        'wallet_balance':new_p.profit,    
                                    }         
                return render(request, 'app/withdrawal.html', data)
        except ObjectDoesNotExist:
            pass
    return render(request, 'app/withdrawal.html')


def oil(request):
    if request.method == "POST":
        username = request.user.username
        choice = request.POST.get('choice')
        data = {
            'already_done': Oil.objects.filter(username__iexact=username).exists(),
        }
        if data['already_done']:
            data['error_message'] = 'sorry you cannot do more than once'
            return JsonResponse(data)
        else:
            Oil.objects.create(
                username = username,
                choice = choice,
            )
    return render(request, 'app/oil.html')

def testimony(request):
    if request.method == "POST":
        testimony = request.POST.get('testmony')
        username = request.user.username
        testimony1 = request.POST.get('testimony1')
        Testimony.objects.create(
                username = username,
                testimony = testimony1,
    

            )
        return HttpResponse('Thank you for sharing your testimony with us')
    return render(request, 'app/testimony.html')


@login_required
def forex(request):
    if request.method == "POST":
        username = request.user.username
        choice = request.POST.get('choice')
        data = {
            'already_done': Forex.objects.filter(username__iexact=username).exists(),
        }
        if data['already_done']:
            data['error_message'] = 'sorry you cannot do more than once'
            return JsonResponse(data)
        else:
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






def faq(request):
    return render(request,'app/faq.html' )

def privacy(request):
    return render(request,'app/privacy.html' )

def terms(request):
    return render(request, 'app/terms.html')

def cancel(request):
    try:
        Cryptocurrency.objects.get (username = request.user.username).delete()
        return HttpResponse('<h2>ok your plan has been canceled successfully</h2>')
    except ObjectDoesNotExist:
        try:
            Forex.objects.get(username = request.user.username).delete()
            return HttpResponse('<h2>ok your plan has been canceled successfully</h2>')
        except ObjectDoesNotExist:
            try:
                Oil.objects.get(username = request.user.username).delete()
                return HttpResponse('<h2>ok your plan has been canceled successfully</h2>')
            except ObjectDoesNotExist:
                 return HttpResponse('<h2>Sorry You do not have a plan yet</h2>')
    return HttpResponse('<h2>ok your plan has been canceled successfully</h2>')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        real_message = '{}, Sender_email: {}, Sender_name: {}'
        sending_message = real_message.format(message,email,name)
        send_mail(subject, sending_message, name, ['contact.galviny@gmail.com'])
    return HttpResponse('sent successfully')
    
def newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        Newsletter.objects.create(
            email = email
        )
    return HttpResponse('sent successfully')
    

def referral_withdrawal(request):
    try:
        payment = Referral_Payment.objects.get(username = request.user.username)
        print ('ask this guy what is payment amount')
        print(payment.amount)
        if payment.amount <= 1000:
            return redirect('withdrawal_failed')
        else:
            Withdraw.objects.create(
                                username = request.user.username,
                                withdraw_amount = payment.amount,
                                date = datetime.datetime.now(),
                            )
            Referrer.objects.filter(referee = request.user.username).delete()
            message = '{} {} made a withdrawal of {} with account number {} and bank {}'
            subject = 'Withdrawal'
            sending = message.format(request.user.profile.firstname, request.user.profile.lastname, payment.amount, request.user.profile.account_number, request.user.profile.bank)
            send_mail(subject, sending, 'Galviny', ['galvinywithdraw@gmail.com'])
            Referrer.objects.filter(referee = request.user.username).delete()
            payment = Referral_Payment.objects.get(username = request.user.username).delete()
            return render (request, 'app/withdrawal-success.html') 
            return HttpResponse('')
    except ObjectDoesNotExist:
        return redirect('withdrawal_failed')
        