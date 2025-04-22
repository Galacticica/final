"""
File: models.py
Author: Reagan Zierke
Date: 2025-04-22
Description: Model for adventures in the bot.
This model represents an adventure that can be completed by a user.
"""


from django.db import models

class Adventure(models.Model):
    idle = models.BooleanField(default=True)
    required_level = models.IntegerField(default=1)
    time_to_complete = models.IntegerField(default=1)
    name = models.CharField(max_length=255)
    description = models.TextField()
    reward_min = models.IntegerField(default=0)
    reward_max = models.IntegerField(default=0)
    xp_min = models.IntegerField(default=0)
    xp_max = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    def __repr__(self):
        return f"Adventure({self.name}, {self.idle}, {self.required_level}, {self.time_to_complete}, {self.reward_min}, {self.reward_max}, {self.xp_min}, {self.xp_max})"