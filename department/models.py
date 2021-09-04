from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Department(models.Model):
    admins = models.ManyToManyField(User)
    name = models.CharField(max_length=60)
    description = models.CharField(max_length=500)
    picture = models.ImageField()
    banner = models.ImageField()
