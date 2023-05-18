
from django.db import models
from django.conf import settings

class Genre(models.Model):
    genre_id = models.IntegerField(unique=True)
    genre_name = models.CharField(max_length=50)

    # def __str__(self):
    #     return str(self.genre_name)
    

class Movie(models.Model):
    movie_id = models.IntegerField()
    title = models.CharField(max_length=100)
    released_date = models.DateField()
    vote_average = models.FloatField()
    overview = models.TextField()
    poster_path = models.CharField(max_length=200)
    # genre_ids = models.ManyToManyField(Genre)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, related_name="comments", on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    rate = models.IntegerField() # 별점표시 # 최대 갯수를 제한해야함 vue에서만 limit걸어놔도 되나?
    movie_comment_like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_movie_comments", blank=True)