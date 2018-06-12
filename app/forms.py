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
    (1, ("Not relevant")),
    (2, ("Review")),
    (3, ("Maybe relevant")),
    (4, ("Relevant")),
    (5, ("Leading candidate")),
    (6, ("Leading candidate"))
    )
    crypto_choice = forms.ChoiceField(choices=STATUS_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Wallet
