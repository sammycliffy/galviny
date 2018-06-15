from django.contrib import admin
from app.models import Plan

# Register your models here.
class Planadmin(admin.ModelAdmin):
    list_display = ['username', 'plan','date', 'amount','confirmed', 'new_date']


admin.site.register(Plan, Planadmin)