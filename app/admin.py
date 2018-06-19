from django.contrib import admin
from app.models import Cryptocurrency, Forex, Oil, Withdraw

# Register your models here.
class Crypto_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date', 'amount_lent']

# Register your models here.
class Forex_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date']

# Register your models here.
class Oil_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date']

# Register your models here.
class withdrawal_admin(admin.ModelAdmin):
    list_display = ['username', 'plan', 'withdraw_amount','date_paid']




admin.site.register(Cryptocurrency, Crypto_admin)
admin.site.register(Forex, Forex_admin)
admin.site.register(Oil, Oil_admin)
admin.site.register(Withdraw, withdrawal_admin)