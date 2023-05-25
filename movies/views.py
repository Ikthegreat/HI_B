from django.shortcuts import render, get_list_or_404, get_object_or_404, redirect
from django.db.models import Q
from rest_framework.response import Response
from operator import itemgetter
# from rest_framework.request import Request
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from .models import *
from accounts.models import *
from accounts.serializers import UserSerializer
from .serializers import (
    MovieListSerializer,
    CommentListSerializer,
    MovieSerializer,
    CommentSerializer,
)
import random
from collections import Counter
import requests
from accounts.models import User, UserSelectMovie
from django.contrib.auth import get_user_model
# Create your views here.


@api_view(["GET", "POST"])
def main(request):
    if request.method == "GET":
        # upcoming data (0,4)
        upcoming_movies = get_list_or_404(Upcoming_movie)
        serializer = MovieListSerializer(upcoming_movies, many=True)
        data = serializer.data
        upcoming_data = random.sample(data, 10)  # upcoming중 5개 선택

        # 사용자 기반 키워드 영화
        user_id = request.user.id
        user_select_movies = UserSelectMovie.objects.filter(user_id=user_id)
        movie_id_lst = []
        for user_select_movie in user_select_movies:
            movie_id = user_select_movie.select_movie_id 
            movie_id_lst.append(movie_id)
        print(movie_id_lst)
        user_select_movies_m = Select_movie.objects.filter(id__in = movie_id_lst)
        # print(user_select_movies_m)
        select_movie_ids = []
        for movie in user_select_movies_m:
            movie_id = movie.movie_id
            select_movie_ids.append(movie_id)
        print(select_movie_ids)
        # print(movie_ids_list)
        # 이제여기서 select_movie 다시 참조해서 filter 걸어서 movie_id 세개 넣기만하면 끝임
        # return JsonResponse(data, safe=False)
        # print(user_select_movies)
        # select_movies = []  # select_movie 객체들을 저장할 리스트

        # for user_select_movie in user_select_movies:
        #     select_movie_id = user_select_movie.select_movie_id
        #     print(select_movie)
        #     print(select_movie)
        #     print(select_movie)
        #     print(select_movie)
        #     # select_movie_id를 사용하여 해당 select_movie를 가져올 수 있습니다
        #     select_movie = Select_movie.objects.get(id=select_movie_id)
        #     select_movies.append(select_movie)  # select_movie를 리스트에 추가

        # select_movies 리스트를 반환
        # return JsonResponse(select_movies, safe=False)
        # select_movies = user.select_movies.values_list('id', flat=True)
        # # return JsonResponse(select_movies, safe=False)
        # response_data = {
        #     "user_id": user.id,
        #     "username": user.username,
        #     "select_movies": list(select_movies)
        # }
        # return JsonResponse(response_data)
        # accounts_user_select_movies의 movie_id들을 리스트로 만들기

        # select_movies의 movie_id들을 리스트로 만들기
        # 위에서 구한 user_movies_list를 활용하여 필요한 작업 수행
        # ...

        # user_info = {
        #     "username": user_name.username,
        #     "user_movies": user_movies_list,
        # }
        # return JsonResponse(user_info)
    


        
        # select_movies = Select_movie.objects.all()
        # select_movie_ids = [movie.movie_id for movie in select_movies]
        # select_movie_ids의 값과 일치하는 keyword_id를 갖는 키워드들을 가져옴
        keywords = Keyword.objects.filter(
            movies__movie_id__in=select_movie_ids
        ).distinct()
        # return JsonResponse(select_movie_ids, safe=False)
        # select_movie_ids의 값과 일치하는 keyword_id를 갖는 키워드들을 가져옴
        keywords = Keyword.objects.filter(
            movies__movie_id__in=select_movie_ids
        ).distinct()
        keyword_ids = list(keywords.values_list("keyword_id", flat=True))
        print(keyword_ids)
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
            if movie_id not in select_movie_ids:
                movie = Movie.objects.get(movie_id=movie_id)
                recommend_data.append({
                    "id": movie.id,
                    "movie_id": movie.movie_id,
                    "poster_path": movie.poster_path,
                    "common_count" : common_count
                })    
        # recommend_data를 공통 요소 개수를 기준으로 내림차순 정렬
        recommend_data = sorted(recommend_data, key=lambda x: x['common_count'], reverse=True)
        recommend_datas = recommend_data[:10]
        # return JsonResponse(recommend_data, safe=False)
        # 상위 5개 추천 결과를 JsonResponse로 반환
        # return JsonResponse(recommend_data[:5], safe=False)
        # recommend_data = sorted(recommend_data, key=itemgetter('common_count'), reverse=True)
        # return JsonResponse(recommend_data, safe=False)
        
        # serializer = MovieListSerializer(all_movies, many=True)
        # serialized_movies = serializer.data

        # nowplaying data (5,9)
        nowplaying_movies = get_list_or_404(Nowplaying_movie)
        serializer = MovieListSerializer(nowplaying_movies, many=True)
        data = serializer.data
        nowplaying_data = random.sample(data, 10)
        # 사람들이 좋아요 많이한 영화 5개
        

        # # Movie 모델의 인스턴스에서 like_movies 필드를 기준으로 movie_id의 빈도를 계산
        # movie_id_counter = Counter(
        #     Movie.like_movies.through.objects.values_list("movie_id", flat=True)
        # )

        # # 빈도가 가장 많은 상위 5개의 movie_id를 추출
        # top_5_movie_ids = [movie_id for movie_id, _ in movie_id_counter.most_common(10)]
        # Movie 모델의 인스턴스에서 like_movies 필드를 기준으로 movie_id의 빈도를 계산
        movie_id_counter = Counter(
            Movie.like_movies.through.objects.values_list("movie_id", flat=True)
        )

        # 빈도가 가장 많은 상위 5개의 movie_id를 추출
        top_10_movie_ids_with_count = [{'movie_id': movie_id, 'count': count} for movie_id, count in movie_id_counter.most_common(10)]

        # top_5_movie_ids_with_count에 대한 추가 정보 추출
        top_10_like_movie = []
        for item in top_10_movie_ids_with_count:
            movie_instance = Movie.objects.get(movie_id=item['movie_id'])
            top_10_like_movie.append({
                "id": movie_instance.id,
                "movie_id": movie_instance.movie_id,
                "poster_path": movie_instance.poster_path,
                "count": item['count']
            })

        # return JsonResponse(top_5_movie_ids, safe=False)
        return JsonResponse((recommend_datas , top_10_like_movie, upcoming_data, nowplaying_data), safe=False)
        # return Response(data)
    elif request.method == "POST":
        serializer = MovieListSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

# @login_required
@api_view(["GET", "POST"])
def select(request):
    # if request.method == "GET":
    #     movies = get_list_or_404(Movie)
    #     select_movies = movies[:20] # 이거 랜덤으로 변경해 줘야댐
    #     serializer = MovieListSerializer(select_movies, many=True)
    #     return Response(serializer.data)
    if request.method == "GET":
        movies = list(Movie.objects.all()[:50])  # 처음 50개의 영화만 가져옴
        random_movies = random.sample(movies, 20)  # 50개 중에서 20개를 무작위로 선택
        serializer = MovieListSerializer(random_movies, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        user = request.user  # 현재 로그인한 사용자의 인스턴스
        UserSelectMovieModel = get_user_model().select_movies.through
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
            user_select_movie = UserSelectMovieModel.objects.create(
                user=user,
                select_movie=select_movie,
            )
        # user = request.user  # 현재 로그인한 사용자의 인스턴스
        # UserSelectMovie = get_user_model().select_movies.through
        # for selected in request.data["movie_id"]:
        #     movie_id = selected
        #     user_id = user.id

        #     user_select_movie = UserSelectMovie.objects.create(
        #         user_id=user_id,
        #         select_movie_id=movie_id,
        #     )
        return Response("Success")
    # elif request.method == "POST":
        # user_id = request.user.id  # 현재 인증된 사용자의 ID를 가져옴

        # for selected in request.data["movie_id"]:
        #     movie = get_object_or_404(Movie, id=selected)

        #     select_movie = UserSelectMovie(
        #         user_id=user_id,
        #         select_movie=movie,
        #     )
        #     select_movie.save()

        # return Response("Success")


        # return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "DELETE", "PUT"])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    # if request.method == "GET":
    #     serializer = MovieSerializer(movie)
    #     print(serializer.data)
    #     return Response(serializer.data)
    if request.method == "GET":
        user_ids = movie.like_movies.values_list("id", flat=True)
        user_movies = (
            Movie.like_movies.through.objects
            .filter(Q(movie_id=movie.movie_id) & Q(user_id__in=user_ids))
            .values_list("user_id", flat=True)
        )
        print({"user_ids" : list(user_movies)})
        serializer_data = {}
        for user in user_movies:
            user = get_object_or_404(get_user_model(), id = user)
            serializer = UserSerializer(user)
            # serializer_data.append(serializer.data)
            print(serializer.data['username'])
            print(serializer.data['profileimage'])
            # if serializer.data['profileimage']:
            serializer_data[serializer.data['username']] = serializer.data['profileimage']
            # else:
                # serializer_data[serializer.data['username']] = 0

        return Response(serializer_data)
        # return Response({"user_ids": list(user_movies)}) # axios요청을 보내게 끔 고쳐야함
    
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


# @api_view(["POST"])
# def comment_movie_like(request, comment_pk):
#     comment = get_object_or_404(Comment, pk=comment_pk)
#     user = request.user
#     if comment.movie_comment_like.filter(pk=user.pk).exists():
#         comment.movie_comment_like.remove(user)
#         serializer = MovieSerializer(comment)
#         return Response(serializer.data)
#     else:
#         comment.movie_comment_like.add(user)
#         serializer = MovieSerializer(comment)
#         return Response(serializer.data)


# # 전체 댓글 serializers
# @api_view(["GET", "POST"])
# def comment_list_or_create(request, movie_pk):
#     def comment_list():
#         comments = get_list_or_404(Comment, movie_id=movie_pk)[::-1]
#         serialiezers = CommentListSerializer(comments, many=True)
#         return Response(serialiezers.data)

#     def create_comment():
#         movie = get_object_or_404(Movie, movie_id=movie_pk)
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save(user=request.user, movie=movie)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#     if request.method == "GET":
#         return comment_list()
#     elif request.method == "POST":
#         return create_comment()


# @api_view(["PUT", "DELETE"])
# def comment_update_or_delete(request, movie_pk, comment_pk):
#     movie = get_object_or_404(Movie, pk=movie_pk)
#     comment = get_object_or_404(Comment, pk=comment_pk)

#     def update_comment():
#         if request.user == comment.user:
#             serializer = CommentSerializer(instance=comment, data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 comments = movie.comments.all()
#                 serializer = CommentSerializer(comments, many=True)
#                 return Response(serializer.data)

#     def delete_comment():
#         if request.user == comment.user:
#             comment.delete()
#             comments = movie.comments.all()
#             serializer = CommentSerializer(comments, many=True)
#             return Response(serializer.data)

#     if request.method == "PUT":
#         if request.user == comment.user:
#             return update_comment()
#     elif request.method == "DELETE":
#         if request.user == comment.user:
#             return delete_comment()
