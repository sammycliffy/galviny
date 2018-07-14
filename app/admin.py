from django.contrib import admin
from app.models import Cryptocurrency, Forex, Oil, Withdraw, Testimony, Referrer

# Register your models here.
class Crypto_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date', 'amount_lent', 'previous_withdraw']

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


admin.site.register(Cryptocurrency, Crypto_admin)
admin.site.register(Forex, Forex_admin)
admin.site.register(Oil, Oil_admin)
admin.site.register(Withdraw, withdrawal_admin)
admin.site.register(Testimony, Testimony_admin)
admin.site.register(Referrer, Referrer_admin)
