from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from rest_framework.response import Response

# from rest_framework.request import Request
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from .models import *
from .serializers import (
    MovieListSerializer,
    CommentListSerializer,
    MovieSerializer,
    CommentSerializer,
)
import random
import requests

# Create your views here.


@api_view(["GET", "POST"])
def main(request):
    if request.method == "GET":
        # upcoming data (0,4)
        upcoming_movies = get_list_or_404(Upcoming_movie)
        serializer = MovieListSerializer(upcoming_movies, many=True)
        data = serializer.data
        random_movies_data = random.sample(data, 5)  # upcoming중 5개 선택

        # 사용자 기반 키워드 영화
        # select_movies = Select_movie.objects.all()
        # select_movie_ids = [movie.movie_id for movie in select_movies]
        # all_movies = Movie.objects.all()
        # serializer = MovieListSerializer(all_movies, many=True)
        # serialized_movies = serializer.data

        # like_keywords = []
        # recommend_movies = []
        # if select_movie_ids:
        #     for movie_id in select_movie_ids:
        #         url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"

        #         headers = {
        #             "accept": "application/json",
        #             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZmQ1M2FlY2QyNzA2ZTk0ODY4MDg1MGQ2ZjU4MTFhNyIsInN1YiI6IjYzZDIwM2NjZmJhNjI1MDA5ZGU5OGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.H_-DEfImhV3nDonoaVeNuu-ya8KT8FxU0wesg-zT0Fg",
        #         }

        #         response = requests.get(url, headers=headers).json()
        #         keywords = response.get("keywords", [])
        #         for keyword in keywords:
        #             like_keywords.append(keyword.get("id"))
        #     movie_ids = [movie["movie_id"] for movie in serialized_movies]
        #     for movie_id in movie_ids:
        #         url = f"https://api.themoviedb.org/3/movie/{movie_id}/keywords"

        #         headers = {
        #             "accept": "application/json",
        #             "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjZmQ1M2FlY2QyNzA2ZTk0ODY4MDg1MGQ2ZjU4MTFhNyIsInN1YiI6IjYzZDIwM2NjZmJhNjI1MDA5ZGU5OGQzOSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.H_-DEfImhV3nDonoaVeNuu-ya8KT8FxU0wesg-zT0Fg",
        #         }
        #         response = requests.get(url, headers=headers).json()
        #         keywords = response.get("keywords", [])
        #         movie_keywords = []
        #         cnt = 0
        #         for keyword in keywords:
        #             movie_keywords.append(keyword.get("id"))
        # for like_keyword in like_keywords:
        #     for movie_keyword in movie_keywords:
        #         if like_keyword == movie_keyword:
        #             cnt += 1
        #     intersection = len(
        #         list(set(like_keywords).intersection(movie_keywords))
        #     )
        #     recommend_movies.append([intersection, movie_id])
        # recommend_movies.sort(reverse=True)
        # return JsonResponse(recommend_movies, safe=False)
        # nowplaying data (5,9)
        nowplaying_movies = get_list_or_404(Nowplaying_movie)
        serializer = MovieListSerializer(nowplaying_movies, many=True)
        data = serializer.data
        nowplaying_data = random.sample(data, 5)
        # 사람들이 좋아요 많이한 영화 5개

        return JsonResponse((random_movies_data, nowplaying_data), safe=False)
        # return Response(data)
    elif request.method == "POST":
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "POST"])
def select(request):
    if request.method == "GET":
        movies = get_list_or_404(Movie)
        select_movies = movies[:20]
        serializer = MovieListSerializer(select_movies, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            selected_movies = serializer.data
            movie_ids = [movie["id"] for movie in selected_movies]  # movie_id로 해야하는가?
            for movie in selected_movies:
                select_movie = Select_movie(
                    movie_id=movie["id"],
                    title=movie["title"],
                    vote_average=movie["vote_average"],
                    overview=movie["overview"],
                    poster_path=movie["poster_path"],
                )
                select_movie.save()
            return Response(
                {"selected_movie_ids": movie_ids}, status=status.HTTP_201_CREATED
            )
            # return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PUT"])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == "GET":
        serializer = MovieSerializer(movie)
        print(serializer.data)
        return Response(serializer.data)

    elif request.method == "DELETE":
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    elif request.method == "PUT":
        serializer = MovieSerializer(movie, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)


@api_view(["POST"])
def like_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    user = request.user
    if movie.like_user.filter(pk=user.pk).exists():
        movie.like_user.remove(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        movie.like_user.add(user)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)


@api_view(["POST"])
def comment_movie_like(request, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    user = request.user
    if comment.movie_comment_like.filter(pk=user.pk).exists():
        comment.movie_comment_like.remove(user)
        serializer = MovieSerializer(comment)
        return Response(serializer.data)
    else:
        comment.movie_comment_like.add(user)
        serializer = MovieSerializer(comment)
        return Response(serializer.data)


# 전체 댓글 serializers
@api_view(["GET", "POST"])
def comment_list_or_create(request, movie_pk):
    def comment_list():
        comments = get_list_or_404(Comment, movie_id=movie_pk)[::-1]
        serialiezers = CommentListSerializer(comments, many=True)
        return Response(serialiezers.data)

    def create_comment():
        movie = get_object_or_404(Movie, movie_id=movie_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    if request.method == "GET":
        return comment_list()
    elif request.method == "POST":
        return create_comment()


@api_view(["PUT", "DELETE"])
def comment_update_or_delete(request, movie_pk, comment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = get_object_or_404(Comment, pk=comment_pk)

    def update_comment():
        if request.user == comment.user:
            serializer = CommentSerializer(instance=comment, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                comments = movie.comments.all()
                serializer = CommentSerializer(comments, many=True)
                return Response(serializer.data)

    def delete_comment():
        if request.user == comment.user:
            comment.delete()
            comments = movie.comments.all()
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data)

    if request.method == "PUT":
        if request.user == comment.user:
            return update_comment()
    elif request.method == "DELETE":
        if request.user == comment.user:
            return delete_comment()
