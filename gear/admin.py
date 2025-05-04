from django.contrib import admin
from .models import Gear

class GearAdmin(admin.ModelAdmin):
    list_display = ('name', 'cost', 'gear_type', 'xp_bonus', 'money_bonus', 'time_bonus')

admin.site.register(Gear, GearAdmin)