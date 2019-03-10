from django.db import models


# Create your models here.
class Equipment(models.Model):
    equip_name = models.CharField(max_length=30)
    equip_rating = models.IntegerField()


class User(models.Model):
    user_name = models.CharField(max_length=30)
    user_password = models.CharField(max_length=30)
    user_rights = models.IntegerField()  # admin - 1, noobie - 0
