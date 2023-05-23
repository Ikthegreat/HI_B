from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from rest_framework.response import Response
from operator import itemgetter
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
        select_movies = Select_movie.objects.all()
        select_movie_ids = [movie.movie_id for movie in select_movies]
        # select_movie_ids의 값과 일치하는 keyword_id를 갖는 키워드들을 가져옴
        keywords = Keyword.objects.filter(
            movies__movie_id__in=select_movie_ids
        ).distinct()
        keyword_ids = list(keywords.values_list("keyword_id", flat=True))
        # 여기서 세개의 movie_id를 filter 활용해서 movie_keyword를 뒤져서 해당 키워드들을 저장함
        # 그 다음에 각각의 movie_id를 돌면서 keyword_id랑 이중 for문 돌면서 같으면 cnt +=1 하고 다돌면
        # cnt랑 movie_id랑 같이 저장해 다돌면 cnt기준으로 sort해서 가장 높은 순대로 5개를 새로운 recommend model에 저장해
        # return JsonResponse(all_movies, safe=False)
        # Movie 모델의 인스턴스를 가져옴
        movies = Movie.objects.all()

        # 각 Movie 인스턴스에 대해 keyword_id를 리스트로 저장할 딕셔너리 생성
        keyword_dict = {}

        # movies를 순회하면서 딕셔너리에 키-값 쌍 추가
        for movie in movies:
            movie_id = movie.movie_id
            keyword_ids1 = movie.keywords.values_list("keyword_id", flat=True)

            # 키워드의 개수가 0인 경우 스킵
            if len(keyword_ids1) == 0:
                continue

            # 이미 해당 movie_id의 키가 딕셔너리에 있는 경우에는 키에 해당하는 리스트에 keyword_ids를 추가
            if movie_id in keyword_dict:
                keyword_dict[movie_id].extend(keyword_ids1)
            # 해당 movie_id의 키가 딕셔너리에 없는 경우에는 새로운 키를 만들고 keyword_ids를 리스트로 초기화
            else:
                keyword_dict[movie_id] = list(keyword_ids1)
        # return JsonResponse(keyword_dict, safe= False)            
        
        recommend_data = []

        # keyword_dict를 순회하면서 공통 요소 개수를 계산
        for movie_id, keyword_id in keyword_dict.items():
            common_keywords = set(keyword_id).intersection(set(keyword_ids))
            common_count = len(common_keywords)
            recommend_data.append({'movie_id': movie_id, 'common_count': common_count})

        # recommend_data를 공통 요소 개수를 기준으로 내림차순 정렬
        recommend_data = sorted(recommend_data, key=lambda x: x['common_count'], reverse=True)

        # 상위 5개 추천 결과를 JsonResponse로 반환
        return JsonResponse(recommend_data[:5], safe=False)
        # recommend_data = sorted(recommend_data, key=itemgetter('common_count'), reverse=True)
        # return JsonResponse(recommend_data, safe=False)
        
        serializer = MovieListSerializer(all_movies, many=True)
        serialized_movies = serializer.data

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
        for selected in request.data["movie_id"]:
            movie = get_object_or_404(Movie, id=selected)
            select_movie = Select_movie(
                movie_id=movie.movie_id,
                title=movie.title,
                vote_average=movie.vote_average,
                overview=movie.overview,
                poster_path=movie.poster_path,
            )
            select_movie.save()
        return Response("Success")
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
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, pk=movie_pk)
        if movie.like_movies.filter(pk=request.user.pk).exists():
            movie.like_movies.remove(request.user)
            is_liked = False
        else:
            movie.like_movies.add(request.user)
            is_liked = True
        context = {
            "is_liked": is_liked,
        }
        return JsonResponse(context)


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
