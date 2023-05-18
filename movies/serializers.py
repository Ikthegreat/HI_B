from rest_framework import serializers
from .models import Movie, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('pk', 'username', 'profile_img',)

class MovieListSerializer(serializers.ModelSerializer):
    class UserSerializer(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = ('pk',)
    like_user = UserSerializer(read_only = True, many = True)

    class Meta:
        model = Movie
        fields = ('id', 'movie_id', 'like_user')

class MovieSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Movie
        fields = '__all__'


class CommentListSerializer(serializers.ModelSerializer):
    
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'updated_at', 'movie', 'user', 'movie_comment_like', "rate" )


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Comment
        fields = '__all__'