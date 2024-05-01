from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    
    _id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    wikiUrl = models.CharField(max_length=100, null=True)
    race = models.CharField(max_length=100, null=True)
    birth = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    death = models.CharField(max_length=100, null=True)
    hair = models.CharField(max_length=100, null=True)
    height = models.CharField(max_length=100, null=True)
    realm = models.CharField(max_length=100, null=True)
    spouse = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name