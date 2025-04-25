from django.db import models
from adventures.models import Adventure

class CustomUser(models.Model):
    discord_id = models.CharField(max_length=255, unique=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    level = models.IntegerField(default=1)
    xp = models.IntegerField(default=0)
    money = models.IntegerField(default=100)

    def __str__(self):
        return self.username
    

class CurrentAdventure(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE)
    time_left = models.IntegerField(default=0)  

    def __str__(self):
        return f"{self.user.username} - {self.adventure.name}"