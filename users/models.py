"""
File: models.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Django models for the Users app.
"""

from django.db import models
from adventures.models import Adventure
from gear.models import Gear

class CustomUser(models.Model):
    '''
    Custom user model for the application.
    This model is used to store user information such as Discord ID, username, level, XP, and money.
    ''' 

    discord_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(default=1)
    xp = models.BigIntegerField(default=0)
    money = models.BigIntegerField(default=100)

    @property
    def xp_needed(self):
        base_xp = 30
        return int(base_xp * (1.2 ** (self.level - 1)))

    def __str__(self):
        user_name = self.username if self.username else "Unknown User"
        return f"{user_name} (ID: {self.discord_id})"
    

class CurrentAdventure(models.Model):
    '''
    Model representing the current adventure of a user.
    Each user can have one current adventure at a time.
    '''

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='current_adventure')
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    time_left = models.IntegerField(default=0)  
    time_started = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        user_name = self.user.username if self.user.username else "Unknown User"
        adventure_name = self.adventure.name if self.adventure and self.adventure.name else "Unknown Adventure"
        return f"{user_name} - {adventure_name}"
    
class OwnedItem(models.Model):
    '''
    Model representing an item owned by a user.
    Each user can own multiple items
    '''

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='owned_items')
    item = models.ForeignKey(Gear, on_delete=models.CASCADE)
