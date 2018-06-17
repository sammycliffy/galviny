from django.contrib import admin
from app.models import Cryptocurrency, Forex, Oil

# Register your models here.
class Crypto_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date']

# Register your models here.
class Forex_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date']

# Register your models here.
class Oil_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit','lent','lend_date']




admin.site.register(Cryptocurrency, Crypto_admin)
admin.site.register(Forex, Forex_admin)
admin.site.register(Oil, Oil_admin)