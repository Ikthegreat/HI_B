from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
# Create your models here.
class User(AbstractUser):
    # symmetrical = False
    follwings = models.ManyToManyField('self', symmetrical=False, related_name= 'followers' ) 
    profile_img = models.TextField(blank=True)