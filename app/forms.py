from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Wallet, Testimony
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth.models import Group


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(max_length=254,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label="Password",widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label="Confirm password",widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2',)
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email already exists')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('firstname', 'lastname', 'address','age', 'sex','occupation','phone', 'account_name','account_number','bank',)

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





from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import Group, User

class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
    
    group_users = forms.ModelMultipleChoiceField(label=u'Usuários deste Grupo', queryset=User.objects.all())

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        users_id = list()
        # Avoid 'No exception supplied' 
        try: 
            users = self.instance.group.user_set.all()
            for u in users:
                users_id.append(u.id)
            if self.fields.has_key('group_users'):
                self.fields['group_users'].initial = users_id
        except Exception:
            pass

    def clean(self):
        group = self.cleaned_data['group']
        group.save()
        if group.user_set.all():
            group.user_set.clear()
        try:
            users = self.cleaned_data['group_users']
            for user in users:
                group.user_set.add(user)
        except:
            return self.cleaned_data
        return self.cleaned_data