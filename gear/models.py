from django.db import models

class Gear(models.Model):
    '''
    Model representing a piece of gear.
    Each piece of gear has a name, type, and stats.
    '''

    name = models.CharField(max_length=255)
    description = models.TextField()
    cost = models.IntegerField(default=0)
    xp_bonus = models.IntegerField(default=0)
    money_bonus = models.IntegerField(default=0)
    time_bonus = models.IntegerField(default=0)