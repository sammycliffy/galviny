"""galviny_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from app import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    url('huikpa/', admin.site.urls,),
    url(r'^$',views.index, name="home"),
    url(r'^index/$',views.index, name="index"),
    url(r'^signup/$', views.signup, name="signup" ),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^login/$', auth_views.login,{'template_name': 'app/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'app/password_reset.html'}, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),
    url(r'^profile_completion/$', views.profile_completion, name="profile_completion"),
    url(r'^sendmail/$',views.send_email, name="email"),
    url(r'^fund-wallet/$',views.fund_wallet, name="fundwallet"),
    url(r'^cryptocurrency/$',views.cryptocurrency, name="cryptocurrency"),
    url(r'^withdrawal/$',views.withdrawal, name="withdrawal"),
    url(r'^testimony/$',views.testimony, name="testimony"),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^forex/$', views.forex, name='forex'),
    url(r'^oil/$', views.oil, name='oil'),
    url(r'^lendmoney/$', views.lendmoney, name='lendmoney'),
    url(r'^success/$', views.withdrawal_success, name='withdrawal_success'),
    url(r'^failed/$', views.withdrawal_failed, name='withdrawal_failed'),
    url(r'^referrer/$', views.referrer, name='referrer'),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^privacy/$', views.privacy, name='privacy'),
    url(r'^terms/$', views.terms, name='terms'),
    url(r'^cancel/$', views.cancel, name='cancel'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^newsletter/$', views.newsletter, name='newsletter'),
    url(r'^referralwithdrawal/$', views.referral_withdrawal, name='referral_withdrawal'),
]

        
