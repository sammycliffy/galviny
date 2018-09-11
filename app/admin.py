from django.contrib import admin
from app.models import Cryptocurrency, Forex, Oil, Withdraw, Testimony, Referrer,Newsletter, Deleted, Referral_Payment
from django.contrib.auth.models import Group


# Register your models here.
class Crypto_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date', 'amount_lent', 'previous_withdraw', 'logistics']

# Register your models here.
class Forex_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date', 'amount_lent', 'previous_withdraw']

# Register your models here.
class Oil_admin(admin.ModelAdmin):
    list_display =['username', 'choice', 'confirmed','profit','lent','lend_date', 'amount_lent', 'previous_withdraw']

# Register your models here.
class withdrawal_admin(admin.ModelAdmin):
    list_display = ['username', 'plan', 'withdraw_amount','previous_withdraw','date', 'logistics']

class Testimony_admin(admin.ModelAdmin):
    list_display = ['username', 'testimony', 'date',]


class Referrer_admin(admin.ModelAdmin):
    list_display = ['referee', 'referred', 'amount','date',]

class Newsletter_admin(admin.ModelAdmin):
    list_display = ['email']

class Deleted_admin(admin.ModelAdmin):
    list_display = ['username','profit']

class Deleted_admin(admin.ModelAdmin):
    list_display = ['username','profit']

class Referral_Pyament_admin(admin.ModelAdmin):
    list_display = ['username','amount', 'previous_username']




admin.site.register(Cryptocurrency, Crypto_admin)
admin.site.register(Forex, Forex_admin)
admin.site.register(Oil, Oil_admin)
admin.site.register(Withdraw, withdrawal_admin)
admin.site.register(Testimony, Testimony_admin)
admin.site.register(Referrer, Referrer_admin)
admin.site.register(Newsletter, Newsletter_admin)
admin.site.register(Deleted, Deleted_admin)
admin.site.register(Referral_Payment, Referral_Pyament_admin)

