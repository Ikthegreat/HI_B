from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Movie
from django.conf import settings

def user_profile_image_path(instance, filename):
        return f'profile_image_{instance.pk}/{filename}'


class User(AbstractUser):
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
    like_movies = models.ManyToManyField(Movie, related_name='like_users', through='MovieLike')
    bookmark_movies = models.ManyToManyField(Movie, related_name='bookmark_users', through='MovieBookmark')

    email = models.EmailField(max_length=254)

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    nickname = models.CharField(max_length=20, blank=True) 
    profile_image = models.ImageField(upload_to='images/', blank=True, null=True) 
    # 문자열 기반 필드는 null True 금지!
    introduce = models.CharField(max_length=100, blank=True)

class MovieLike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class MovieBookmark(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)