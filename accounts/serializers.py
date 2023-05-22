from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie
from accounts.models import *

# from movies.serializers import MovieSerializer
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        class Meta:
            model = Movie
            fields = "__all__"

    likes_movies = MovieSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "profile_img",
            "followings",
            "followers",
            "like_movies",
        )


class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = "__all__"


class UserImgSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_img", "id")
