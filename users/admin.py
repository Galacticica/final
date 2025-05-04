from django.contrib import admin
from .models import CustomUser, CurrentAdventure, OwnedItem

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('discord_id', 'username', 'level', 'xp', 'money')
    search_fields = ('discord_id', 'username')
    list_filter = ('level',)
    ordering = ('-level',)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('discord_id', 'username')
        }),
        ('Stats', {
            'fields': ('level', 'xp', 'money')
        }),
    )
    readonly_fields = ('discord_id',)

class CurrentAdventureAdmin(admin.ModelAdmin):
    list_display = ('user', 'adventure', 'time_left', 'time_started')
    search_fields = ('user__username', 'adventure__name')
    list_filter = ('adventure',)
    ordering = ('-time_left',)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('user', 'adventure')
        }),
        ('Time Left', {
            'fields': ('time_left', 'time_started')
        }),
    )

class OwnedItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item')
    search_fields = ('user__username', 'item__name')
    list_filter = ('item',)
    ordering = ('-user',)
    list_per_page = 20
    fieldsets = (
        (None, {
            'fields': ('user', 'item')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CurrentAdventure, CurrentAdventureAdmin)
admin.site.register(OwnedItem, OwnedItemAdmin)
