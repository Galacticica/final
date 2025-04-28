"""
File: models.py
Author: Reagan Zierke
Date: 2025-04-27
Description: Django models for the Users app.
"""



from django.db import models
from adventures.models import Adventure
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from django.db.models.fields.related_descriptors import ReverseOneToOneDescriptor


class CustomUser(models.Model):
    '''
    Custom user model for the application.
    This model is used to store user information such as Discord ID, username, level, XP, and money.
    '''

    discord_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    money = models.IntegerField(default=100)

    current_adventure: 'ReverseOneToOneDescriptor'

    def __str__(self):
        return self.username
    

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
        return f"{self.user.username} - {self.adventure.name}"