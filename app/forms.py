from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Wallet


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname', 'address','age', 'sex')

class WalletForm (forms.Form):
    STATUS_CHOICES = (
    (1, ("50,000   = 1,200 profit daily")),
    (2, ("100,000  = 2,400 profit daily")),
    (3, ("200,000  = 4,800 profit daily")),
    (4, ("300,000  = 7,200 profit daily")),
    (5, ("400,000  = 9,600 profit daily")),
    (6, ("500,000  = 12,800 profit daily")),
    (7, ("1,000,000  = 24,000 profit daily"))
    )
    crypto_choice = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Wallet
