from django.contrib import admin
from app.models import Cryptocurrency

# Register your models here.
class Crypto_admin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed','profit']


admin.site.register(Cryptocurrency, Crypto_admin)