# from django.shortcuts import render, get_object_or_404, get_list_or_404
# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from django.contrib.auth import get_user_model
# from .serializers import ProfileSerializer, UserImgSerializer, UserSerializer
# from rest_framework.response import Response


# @api_view(["GET"])
# def profile_with_like_movies(request, username):
#     profile_user = get_object_or_404(get_user_model(), username=username)
#     profile = profile_user.profile
#     serializer = ProfileSerializer(profile)
#     return Response(serializer.data)


# @api_view(["GET", "PUT"])
# def upload_img(request, username):
#     user = get_object_or_404(get_user_model(), username=username)

#     if request.method == "GET":
#         serializer = UserImgSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     elif request.method == "PUT":
#         if request.user != user:
#             return Response({"profile": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

#         serializer = UserImgSerializer(user, data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)


# @api_view(["GET"])
# def profile_with_comment(request, username):
#     profile_user = get_object_or_404(get_user_model(), username=username)
#     profile = profile_user.profile
#     serializer = ProfileSerializer(profile)
#     return Response(serializer.data)


# @api_view(["POST"])
# def follow(request, username):
#     user = get_object_or_404(get_user_model(), username=username)
#     if user != request.user:
#         if user.followers.filter(pk=request.user.pk).exists():
#             user.followers.remove(request.user)
#             followed = False
#         else:
#             user.followers.add(request.user)
#             followed = True
#     context = {
#         "followed": followed,
#     }
#     serializer = UserSerializer(user)
#     return Response(serializer.data)


# @api_view(["GET"])
# def get_my_profile(request):
#     user = get_object_or_404(get_user_model())
#     me = request.user
#     profile = me.profile

#     serializer = ProfileSerializer(profile)
#     return Response(serializer.data)


# @api_view(["GET"])
# def user_profile(request, username):
#     user = get_object_or_404(get_user_model(), username=username)
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# @api_view(["POST", "PUT"])
# def update_profile(request, username):
#     profile_user = get_object_or_404(get_user_model(), username=username)
#     me = request.user
#     if request.method == "PUT":
#         profile = profile_user.profile
#         if me == profile_user:
#             serializer = ProfileSerializer(instance=profile, data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save()
#                 return Response(serializer.data)

#     if request.method == "POST":
#         if me == profile_user:
#             serializer = ProfileSerializer(data=request.data)
#             if serializer.is_valid(raise_exception=True):
#                 serializer.save(user=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
from django.shortcuts import render, get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserImgSerializer
from movies.models import Movie
from movies.serializers import MovieSerializer
# from .models import Comment, Profile
from rest_framework.response import Response


@api_view(["GET", "PUT"])
def upload_img(request, username):
    user = get_object_or_404(get_user_model(), username=username)

    if request.method == "GET":
        serializer = UserImgSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        if request.user != user:
            return Response({"profile": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = UserImgSerializer(user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def follow(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            followed = False
        else:
            user.followers.add(request.user)
            followed = True
    context = {
        "followed": followed,
    }
    # return Response(context, status=status.HTTP_200_OK)
    serializer = UserSerializer(user)
    return Response(serializer.data)


# @api_view(["GET"])
# def user_profile(request, username):
#     user = get_object_or_404(get_user_model(), username=username)
#     id = user.id
#     if request.method == "GET":
#         serializer = UserSerializer(user)
#         return Response(serializer.data)

@api_view(["GET"])
def user_profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    user_movies = user.like_movies.values_list("movie_id", flat=True)  # 해당 사용자의 좋아하는 영화의 movie_id 목록
    movies = Movie.objects.filter(movie_id__in=user_movies)  # movie_id 목록에 해당하는 영화들을 가져옴

    serializer = MovieSerializer(movies, many=True)  
    print(serializer.data)
    return Response(serializer.data)
