from django.urls import path
from . import views


urlpatterns = [
    # path('', views.start), # 시작화면
    path('main/', views.main), # main 화면
    # path('select/', views.select), # 영화 선택창
    path('main/<int:movie_pk>/', views.movie_detail), # 영화 detail
    path('main/<int:movie_pk>/like/', views.like_movie), # 영화 좋아요
    path('main/<int:movie_pk>/comments/', views.comment_list_or_create), # 영화 댓글
    path('main/<int:movie_pk>/comments/<int:comment_pk>/', views.comment_update_or_delete), # 영화 update or delete
]
