"""
File: models.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Model for adventures in the bot.
This model represents an adventure that can be completed by a user.
"""

from django.db import models

class Adventure(models.Model):
    '''
    Model representing an adventure that can be completed by a user.
    Each adventure has a name, description, required level, time to complete,
    '''
    
    idle = models.BooleanField(default=True)
    required_level = models.IntegerField(default=1)
    time_to_complete = models.BigIntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    reward_min = models.BigIntegerField(default=0)
    reward_max = models.BigIntegerField(default=0)
    xp_min = models.BigIntegerField(default=0)
    xp_max = models.BigIntegerField(default=0)

    def save(self, *args, **kwargs):
        '''
        Saves reward and xp values based on the required level.
        '''

        xp = int(30 * (1.2 ** (self.required_level - 0.5)))
        self.xp_min = int(xp * 0.4)
        self.xp_max = int(xp * 0.55)

        money = 40 + ((self.required_level - 1) * 15)
        self.reward_min = int(money * 0.75)
        self.reward_max = int(money * 1.25)

        self.time_to_complete = int(25 * self.required_level ** 2 + 125)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Adventure({self.name}, {self.idle}, {self.required_level}, {self.time_to_complete}, {self.reward_min}, {self.reward_max}, {self.xp_min}, {self.xp_max})"