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
            'armor':     {'xp_bonus': 0.375, 'money_bonus': 0.1125, 'time_bonus': 0.055},
            'weapon':  {'xp_bonus': 0.1875, 'money_bonus': 0.375, 'time_bonus': 0.03},
            'accessory':   {'xp_bonus': 0.1125, 'money_bonus': 0.1875, 'time_bonus': 0.2},
        }

        points = self.cost / 75

        multipliers = gear_type_modifiers.get(self.gear_type)

        self.xp_bonus = round(points * multipliers['xp_bonus'], 2)
        self.money_bonus = round(points * multipliers['money_bonus'], 2)
        self.time_bonus = round(points * multipliers['time_bonus'], 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name