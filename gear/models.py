from django.db import models

class Gear(models.Model):
    '''
    Model representing a piece of gear.
    Each piece of gear has a name, type, and stats.
    '''

    name = models.CharField(max_length=255)
    description = models.TextField()
    gear_type = models.CharField(
        max_length=50,
        choices=[
            ('weapon', 'Weapon'),
            ('armor', 'Armor'),
            ('accessory', 'Accessory'),
        ],
        default='weapon'
    )
    cost = models.IntegerField(default=0)
    xp_bonus = models.FloatField(default=0.0)
    money_bonus = models.FloatField(default=0.0)
    time_bonus = models.FloatField(default=0.0)

    def save(self, *args, **kwargs):
        '''
        Saves the gear item.
        '''

        gear_type_modifiers = {
            'armor':     {'xp_bonus': 0.5, 'money_bonus': 0.15, 'time_bonus': 0.25},
            'weapon':  {'xp_bonus': 0.25, 'money_bonus': 0.5, 'time_bonus': 0.15},
            'accessory':   {'xp_bonus': 0.15, 'money_bonus': 0.25, 'time_bonus': 0.5},
        }

        points = self.cost // 50

        multipliers = gear_type_modifiers.get(self.gear_type)

        self.xp_bonus = round(points * multipliers['xp_bonus'], 1)
        self.money_bonus = round(points * multipliers['money_bonus'], 1)
        self.time_bonus = round(points * multipliers['time_bonus'], 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name