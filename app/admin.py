from django.contrib import admin
from app.models import Cryptocurrency

# Register your models here.
class Planadmin(admin.ModelAdmin):
    list_display = ['username', 'choice', 'confirmed',]


admin.site.register(Cryptocurrency, Planadmin)