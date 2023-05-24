# from django.db import models
# from django.contrib.auth.models import AbstractUser
# from movies.models import Movie
# from django.conf import settings

# def user_profile_image_path(instance, filename):
#         return f'profile_image_{instance.pk}/{filename}'


# class User(AbstractUser):
#     followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')
#     like_movies = models.ManyToManyField(Movie, related_name='like_users', through='MovieLike')

# class Profile(models.Model):
#     user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     nickname = models.CharField(max_length=20, blank=True)
#     profile_image = models.ImageField(upload_to='images/', blank=True, null=True)
#     introduce = models.CharField(max_length=100, blank=True)

# class MovieLike(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Select_movie, Movie
# Create your models here.


class User(AbstractUser):
    followings = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers"
    )
    profileimage = models.ImageField(blank=True)
    select_movies = models.ManyToManyField(Select_movie, through='UserSelectMovie', related_name="select_movies")
    # select_movies = models.ManyToManyField(Select_movie, related_name="select_movies")

class UserSelectMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    select_movie = models.ForeignKey(Select_movie, on_delete=models.CASCADE)